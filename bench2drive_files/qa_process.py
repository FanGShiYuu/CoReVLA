import math
from io_utils import *
from waypoint_decoder import decode_xy_token, decode_polar_token
from waypoint_extractor import get_waypoint_dict_seq_from_rel
from generator_modules import SpeedCommand, DirectionCommand

def generate_condition(anno_path, qid, special_state_str=None):
    anno = load_json_gz(get_real_path(anno_path))
    condition = ""
    # condition += "All images are taken from the ego vehicle's perspective. "
    if qid in [18, 19]:
        condition += "\"\"\"In this question, focus on specific objects rather than general categories. " +\
        "For example, if you need to address vehicles on the road, the answer should specify which vehicle.\"\"\""
    if qid in [
        10, # Does the ego vehicle need to change lanes ... due to obstruction?
        12, # Does the ego vehicle need to change lanes ... other than circumventing obstruction?
        13, # Must the ego vehicle change lane or deviate from the lane now? why?
        8, # Does the ego vehicle need to brake? Why?
        18, # What are the important objects in the scene?
        19, # What are the important objects in the scene? List them from most to least important.
        29, # List potential overlap vehicles.
        42, # Predict future waypoints.
        43, # Natural language description of future motion.
        50, # High-level command for navigation
    ]:
        if qid in [42]:
            condition += "The ego vehicle is driving at the speed of " +\
                    f"{anno['speed']:.1f} m/s. "
        else:
            condition += "The ego vehicle is driving at the speed of " +\
                        f"{anno['speed']:.1f} m/s, and it wants to "
            
            distance_to_command_near = math.sqrt(math.pow((anno['x_command_near'] - anno['x']), 2) + math.pow((anno['y_command_near'] - anno['y']), 2))

            distance_to_command_far = math.sqrt(math.pow((anno['x_command_far'] - anno['x']), 2) + math.pow((anno['y_command_far'] - anno['y']), 2))

            command_map = {
                        1: 'turn left at the intersection',
                        2: 'turns right at the intersection',
                        3: 'drive straight at the intersection',
                        4: 'follow the road',
                        5: f'do a lane change to the left',
                        6: f'do a lane change to the right',
                    }

            command_str = "follow the road"

            if anno['command_far'] in [1, 2, 3, 5, 6] and distance_to_command_far < 20.0:
                command_str = command_map[anno['command_far']]
            if anno['command_near'] in [1, 2, 3, 5, 6] and distance_to_command_near < 20.0:
                command_str = command_map[anno['command_near']]
            if special_state_str is not None and special_state_str != "":
                command_str = special_state_str
            condition += command_str
            condition += ". "

        if qid in [
            17, # Where is {other_vehicle_location_description} going?
            16, # What is the moving status of {other_vehicle_location_description}?
            9, # What should the ego vehicle do based on the {actor_type}?
            14, # The list of traffic lights and signs affecting the ego vehicle in current scene is: {sign_list_str}. Based on these traffic signs, what actions should the ego vehicle take respectively?
            20, # Where on the road is {vehicle_description} located?
            21, # What is the rough moving speed and moving direction of {vehicle_description}?
            22, # What is the exact moving speed and moving direction of {vehicle_description}?
            23, # The ego vehicle {command_str}. Is {vehicle_location_description} potentially crossing the path of the ego vehicle?
            24, 25, 26, 27, 28, 29, # The important vehicles are ...
        ]:
            condition += "\"\"\"Notice that in the following questions, the parentheses after the object contain its ID and the name of the camera that can see it.\"\"\" "

        if qid in [43]:  # TODO fangshiyuu modified it at 0711, cause vlms seems overly care speed match therefore to stop even great distance between ego and front
            condition = "Following these steps to make a driving decision: " +\
                    "1. Identify vehicles in the same lane as the ego vehicle by checking: (1) their speed direction relative to ego is within ±40° (0°=same direction), " +\
                    " (2) their lateral distance (left/right) is ≤2.5m. Output the vehicle's id in the same lane with ego vehicle \n" +\
                    "2. From these same-lane vehicles, find the most dangerous preceding vehicle (must be in front of ego vehicle that is has 'Xm to the front' in relative position) by calculating TTC (Time To Collision = longitudinal distance / speed difference). " +\
                    " Output the most dangerous preceding vehicle's id, if there is no front vehicle, you can directly choose to ACCELERATE \n" +\
                    "3. Based on the already identified most dangerous preceding vehicle in the same lane (from previous analysis, prioritizing safety while maximizing efficiency. " +\
                    " You need to understand that your decision-making frequency is once per second, so you must think ahead when making decisions. " +\
                    " (1) If the preceding vehicle is moving, adjust speed based on their TTC (e.g., decelerate if TTC < 3s, stop if TTC < 2s, Only check TTC when ego speed large than preceding vehicle speed). " +\
                    " (2) If the preceding vehicle is stationary, evaluate a lane change for overtaking (only proceed after ensuring no collision risk in neighboring lanes; otherwise, stop and wait for a safe opportunity)." +\
                    " (3) If there is no preceding vehicle, you can ACCELERATE" 


            # condition = "For vehicles in the same lane (lateral offset within lane width), calculate time gap (distance/relative_speed). " +\
            #     "ACCELERATE when ego is slower than the front vehicle and the time gap is comfortably large. " +\
            #     "DECELERATE when ego is faster than the front vehicle and the time gap is tightening. " +\
            #     "Adjust braking intensity based on how rapidly the time gap decreases (emergency braking if closing too fast)."

            # condition += "Accelerate when ego speed is lower than the closest front vehicle (smallest X value in Xm to the front) and distance exceeds one car length. " +\
            #              "Maintain speed when ego speed matches the front vehicle. " +\
            #              "Decelerate when ego speed exceeds the front vehicle at close distances."


            # condition += "Please ensure that the speed of the ego vehicle matches " +\
            #              "that of surrounding normally moving vehicles under normal circumstances to avoid low traffic efficiency."
    return condition

def process_qa_by_qid(question, gt, qid):
    
    new_q = question

    if qid == 24:
        new_q = "Forget the above actors of other vehicles, what is your current action based on the questions you answer before, only based on the image input, double check is there any stop sign, obstacles, traffic light or cyclists that very close to you now, will they affect your current actions?" +\
                "Determine the required actions accordingly if your current action are affected. You can consider following principles: "+\
                "(1) When meeting red light, of course stop and wait for green light then accelerate, " +\
                "(2) When meeting static obstacles, change lane (do it when you are sure that you will not collide with vehicle on other lane you plan to change), " +\
                "(3) When meeting stop sign, stop if you have speed now and accelerate if you have stopped, "    

                # new_q = "What are the rough moving speed and moving direction of the important vehicles?"  # TODO
    if qid == 25:
        new_q = "What are the exact moving speed and moving direction of the important vehicles?"
    if qid == 26:
        new_q = "Infer the important vehicles, rank their importance and determine their locations on the road."
    if qid == 27:
        new_q = "Where on the road are the important vehicles located? Try to determine their lanes relative to the ego vehicle."
    if qid == 28:
        new_q = "Identify important vehicles that may overlap with " +\
                "the ego vehicle's path, and explain the reasons."
    if qid == 29:
        new_q = "Identify important vehicles that may overlap with " +\
                "the ego vehicle's path."
    if qid == 47:
        new_q = "Identify important vehicles that may overlap with " +\
                "the ego vehicle's path, explain the reasons, " +\
                "and determine actions that could cause a collision."
    if qid == 46:
        new_q = "Identify important vehicles that may overlap with " +\
                "the ego vehicle's path " +\
                "and determine actions that could cause a collision."
    if qid == 42:
        new_q = "Please predict the waypoint tokens for the next 4 seconds, " +\
                "with one set every 0.5 seconds, " +\
                "for a total of 8 sets of relative displacements."
    if qid == 50:  # TODO fangshiyu modified
        new_q = "Forget the above actors of other vehicles, only using the previously chose correct action from above questions (do not re-decide). Provide the appropriate behaviour for the ego vehicle according to the previously chose correct action," +\
            "Final output must consist of two keys:" +\
            "Direction key: 'FOLLOW_LANE'/'CHANGE_LANE_LEFT'/'CHANGE_LANE_RIGHT' (road navigation)," +\
            "'GO_STRAIGHT'/'TURN_LEFT'/'TURN_RIGHT' (junction navigation)," +\
            "'DEVIATE_LEFT'/'DEVIATE_RIGHT' (lane position adjustment)." +\
            "Speed key: 'KEEP'/'ACCELERATE'/'DECELERATE'/'STOP'." +\
            "MUST provide Direction and Speed Keys AT THE END. for example: Direction: FOLLOW_LANE, Speed Keys: KEEP (Speed key must choose from 'KEEP'/'ACCELERATE'/'DECELERATE'/'STOP')" 
            # "MUST provide previously chose correct action, Direction and Speed Keys AT THE END, like: My Previously Chose Correct Action: XXX, Direction: XXX, Speed Keys (Must choose from 'KEEP'/'ACCELERATE'/'DECELERATE'/'STOP'): XXX"
            
            # "Identify the most relevant front vehicle by calculating the smallest time gap (distance/speed) among vehicles" +\
            # "in the same lane and moving to the same direction (vehicles with lateral offset >3m from ego are considered in different lanes)." +\
            # "If your speed is lower than the identified front vehicle AND time gap >2 seconds AND space gap >5m, consider 'ACCELERATE'. Then consider 'KEEP', 'ACCELERATE', 'DECELERATE', or 'STOP'" +\

        # new_q = "Provide the appropriate behaviour for the ego vehicle," +\
        #         "Identify the closest front vehicle in the same lane with you (must have 'to the front' in relative position) with the smallest distance value (X in 'Xm to the front'),"  +\
        #         "if your speed lower than the the closest front vehicle and gap is larger than 5m, consider ACCELERATE"  +\
        #         "final output should consists of two keys: the Direction key, which can be " +\
        #         "'FOLLOW_LANE', 'CHANGE_LANE_LEFT', 'CHANGE_LANE_RIGHT'(these three are for situations following a road), " +\
        #         "'GO_STRAIGHT', 'TURN_LEFT', 'TURN_RIGHT'(these three are for situations in a junction), " +\
        #         "'DEVIATE_LEFT' or 'DEVIATE_RIGHT'(these two are used when the ego vehicle wants to occupy a position slightly to the left/right within the current lane). " +\
        #         "and the Speed key, which can be 'KEEP', 'ACCELERATE', 'DECELERATE', or 'STOP'. " +\
        #         "You MUST provide the Direction Key and Speed Key AT THE END of the answer with NO OTHER WORD FOLLOWING; otherwise, the answer will be considered broken. " #  +\
        #         # "format example (if you want to follow the lane at current speed): Direction Key = FOLLOW_LANE, Speed Key = KEEP"

    # decide to leave gt modification to evaluation module
    # preserve original gt to make use of full information
    new_a = gt

    return new_q, new_a

def process_answer_by_qid(answer, qid, wp_code):
    new_a = answer
    if qid == 42:
        if wp_code:
            if wp_code == "xy":
                xy_decd = decode_xy_token(answer)
                a_json = get_waypoint_dict_seq_from_rel(xy_decd)
                new_a = json.dumps(a_json)
            elif wp_code == "ds":
                ds_decd = decode_polar_token(answer)
                a_json = get_waypoint_dict_seq_from_rel(ds_decd)
                new_a = json.dumps(a_json)

    return new_a

def is_frame_trivial(vqa_json_dict):
    return vqa_json_dict['extra_flags'].get('is_trivial_case', False)

def is_frame_red_light(vqa_json_dict):
    return vqa_json_dict['extra_flags'].get('waiting_for_red_light', False)

def is_good_case(vqa_json_dict, filter_trivial=False, filter_red_light=False):
    all_flags = [
        'ego_speed',
        'change_lane_flag',
        'change_lane_gt',
        'speed_cmd',
        'direction_cmd',
        'speed_change_gt',
        'waiting_for_red_light',
        'is_trivial_case'
    ]

    extra_flags = vqa_json_dict['extra_flags']
    for flag in all_flags:
        if flag not in extra_flags:
            print_error(f"Flag '{flag}' does not exist in data, can not filter. This frame is neglected.")
            return False

    reserve_flag = True

    if filter_trivial and extra_flags['is_trivial_case']:
        return False
    
    if filter_red_light and extra_flags['waiting_for_red_light']:
        return False
    
    ego_speed = extra_flags['ego_speed']
    change_lane_flag = extra_flags['change_lane_flag']
    change_lane_gt = extra_flags['change_lane_gt']
    final_spd_cmd = extra_flags['speed_cmd']
    final_dir_cmd = extra_flags['direction_cmd']
    speed_change_gt = extra_flags['speed_change_gt']

    all_spd_cmd = SpeedCommand()
    all_dir_cmd = DirectionCommand()

    # speed_change_gt in ["Ambiguous", "Accelerate", "Decelerate", "Constant"]

    if not (change_lane_flag and change_lane_gt):
        if speed_change_gt == 'Accelerate' and final_spd_cmd == all_spd_cmd.decelerate:
            return False
        if speed_change_gt == 'Decelerate' and final_spd_cmd == all_spd_cmd.accelerate:
            return False

    if (change_lane_flag == True and change_lane_gt == False) or \
       (ego_speed > 3.0 and change_lane_flag != change_lane_gt):
        return False

    return reserve_flag

def transfer_question_in_cot(Q, qid):
    new_q = Q
    if qid == 19:
        new_q = "Rank the important objects in the scene " +\
                "from most to least important."
    if qid == 15:
        # new_q = "Based on the image input, double check is there any stop sign or traffic light now, will they affect your current actions?" +\
        #         "Determine the required actions accordingly if there is stop sign or traffic light now."
        new_q = "Identify all traffic lights and signs affecting the ego vehicle " +\
                "and determine the required actions accordingly."
    if qid == 24:
        new_q = "Estimate the rough speed and direction of the important vehicles."
    if qid == 25:
        new_q = "Infer the exact speed and direction of the important vehicles."
    if qid == 26:
        new_q = "Infer the important vehicles and determine their locations on the road."
    if qid == 27:
        new_q = "Infer the important vehicles' locations on the road."
    if qid == 28:
        new_q = "Identify important vehicles that may overlap with " +\
                "the ego vehicle's path, and explain the reasons."
    if qid == 29:
        new_q = "Identify important vehicles that may overlap with " +\
                "the ego vehicle's path."
    if qid == 47:
        new_q = "Identify important vehicles that may overlap with " +\
                "the ego vehicle's path, explain the reasons, " +\
                "and determine actions that could cause a collision."
    if qid == 46:
        new_q = "Identify important vehicles that may overlap with " +\
                "the ego vehicle's path " +\
                "and determine actions that could cause a collision."
    if qid == 8:
        new_q = "Determine whether the ego vehicle needs to brake."
    if qid == 13:
        new_q = "Determine whether the ego vehicle needs to change lane or " +\
                "deviate from the current lane."
    if qid == 43:
        new_q = "Determine the correct action for the ego vehicle to take now."
    if qid == 50:
        new_q = "Provide the appropriate action for the ego vehicle " +\
                "using the direction key and speed key."
    
    new_q = f"**{new_q}**\n"
    
    return new_q

def transfer_answer_in_cot(A, qid):
    new_a = A

    def remove_last_notnow(text: str) -> str:
        sentences = text.split('. ')
        if sentences[-1].startswith("But not now"):
            sentences.pop()
        final_sentence = '. '.join(sentences)
        if not final_sentence.endswith('.'):
            final_sentence += '.'
        return final_sentence

    if qid == 13: # in this stage, needn't infer 'not now's.
        new_a = remove_last_notnow(A)
    
    new_a = f"{new_a}\n"

    return new_a

def answer_is_trivial(A, qid):
    if qid in [18, 19, 24, 25, 26, 27, 46, 47]:
        return A.startswith("There is no important object in the scene.") or \
               A.startswith("There's no important vehicle in the current scene.") or \
               A.startswith("There's no important vehicle")
    if qid in [2]:
        return A == "No, the ego vehicle is not affected by a stop sign."
    if qid in [3]:
        return A == "No, the ego vehicle is not affected by a speed limit sign."
    if qid in [4]:
        return A == "There's no traffic sign affecting the ego vehicle."
    if qid in [5]:
        return A == "No, the ego vehicle is not affected by a traffic light."
    if qid in [6]:
        return A == "There is no traffic light affecting the ego vehicle."
    if qid in [7]:
        return A == "There's no speed limit now."
    if qid in [40, 41]:
        return A == "There's no serious potential hazard apart from them."
    if qid in [15]:
        return A == "There's no traffic light or sign affecting the ego vehicle right now."
    return False
    
def get_trivial_ratio(qid):
    if qid in [18, 19, 24, 25, 26, 27, 46, 47]:
        return 0.1
    if qid in [2, 3, 4, 5, 6, 7, 15]:
        return 0.4
    if qid in [40, 41]:
        return 0.2
    return 1.0

def find_qdict_by_id(qid, vqa_data):
    """
    Given qid, return lists of question ans gt answers.
    """
    alllist = []

    vqa_content = vqa_data['QA']
    if isinstance(vqa_content, dict):
        for categories in vqa_content.values():
            for qdict in categories:
                if 'qid' in qdict and qdict['qid'] == qid:
                    alllist.append(qdict)
    elif isinstance(vqa_content, list):
        for qdict in vqa_content:
            if 'qid' in qdict and qdict['qid'] == qid:
                alllist.append(qdict)
    
        
    if len(alllist) == 0:
        print_error(f'Error: Question with qid {qid} not found. Ignored.')

    return alllist