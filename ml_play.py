"""
The template of the main script of the machine learning process
"""

import games.arkanoid.communication as comm
from games.arkanoid.communication import ( \
    SceneInfo, GameStatus, PlatformAction
)

def ml_loop():
    """
    The main loop of the machine learning process

    This loop is run in a separate process, and communicates with the game process.

    Note that the game process won't wait for the ml process to generate the
    GameInstruction. It is possible that the frame of the GameInstruction
    is behind of the current frame in the game process. Try to decrease the fps
    to avoid this situation.
    """

    # === Here is the execution order of the loop === #
    # 1. Put the initialization code here.
    ball_served = False

    # 2. Inform the game process that ml process is ready before start the loop.
    comm.ml_ready()

    # 3. Start an endless loop.
    while True:
        # 3.1. Receive the scene information sent from the game process.
        scene_info = comm.get_scene_info()

        # 3.2. If the game is over or passed, the game process will reset
        #      the scene and wait for ml process doing resetting job.
        if scene_info.status == GameStatus.GAME_OVER or \
            scene_info.status == GameStatus.GAME_PASS:
            # Do some stuff if needed
            ball_served = False

            # 3.2.1. Inform the game process that ml process is ready
            comm.ml_ready()
            continue

        # 3.3. Put the code here to handle the scene information

        # 3.4. Send the instruction for this frame to the game process
        if not ball_served:
            comm.send_instruction(scene_info.frame, PlatformAction.SERVE_TO_LEFT)
            ball_served = True
            bounce_to_left = False
            bounce_to_right = False
            distance = 0
            direction_x = -1 #-1 for left , 1 for right
            direction_y = 1  #-1 for down , 1 for up
            init_x = 100
            init_y = 402
        else:
            ball_x = scene_info.ball[0]
            ball_y = scene_info.ball[1]
            platform_x = scene_info.platform[0]
            platform_y = scene_info.platform[1]      

            if ball_x == 0:
                direction_x = 1
            elif ball_x == 195:
                direction_x = -1
            if ball_y - init_y < 0:               
                direction_y = 1
            else:
                direction_y = -1

            init_x = ball_x
            init_y = ball_y

            if platform_y - ball_y > 285:
                bounce_to_left = False
                bounce_to_right = False
                distance = 0                                              
                # modify        
                if platform_x < 75:
                    comm.send_instruction(scene_info.frame, PlatformAction.MOVE_RIGHT)
                elif platform_x > 75:
                    comm.send_instruction(scene_info.frame, PlatformAction.MOVE_LEFT)      

            elif (platform_y - ball_y <= 285 and platform_y - ball_y > 200 and direction_y == -1):
                if direction_x == 1:
                    if ball_x <= 200 - (platform_y - ball_y - 200):
                        bounce_to_right = False
                        bounce_to_left = True                    
                        distance = (platform_y - ball_y) - (195 - ball_x)                                        
                    elif ball_x > 200 - (platform_y - ball_y - 200):
                        bounce_to_right = True
                        bounce_to_left = False
                        distance = (platform_y - ball_y) - 195 - (195 - ball_x)
                elif direction_x == -1:
                    if ball_x >= platform_y - ball_y - 200:
                        bounce_to_right = True
                        bounce_to_left = False
                        distance = (platform_y - ball_y) - ball_x
                    elif ball_x < platform_y - ball_y - 200:
                        bounce_to_right = False
                        bounce_to_left = True 
                        distance = (platform_y - ball_y) - 195 - ball_x
            elif platform_y - ball_y <= 200 and direction_y == -1:
                if direction_x == 1:
                    if (platform_y - ball_y) + ball_x <= 200:
                        bounce_to_right = True
                        bounce_to_left = False
                        distance = ball_x + (platform_y - ball_y)
                    elif (platform_y - ball_y) + ball_x > 200:
                        bounce_to_left = False
                        bounce_to_right = True         
                        distance = 195 - (platform_y - ball_y) + (195 - ball_x)
                if direction_x == -1:
                    if (platform_y - ball_y) <= ball_x:
                        bounce_to_right = True
                        bounce_to_left = False 
                        distance = ball_x - (platform_y - ball_y)
                    elif (platform_y - ball_y) > ball_x:
                        bounce_to_left = False
                        bounce_to_right = True         
                        distance = (platform_y - ball_y) - ball_x    

            if bounce_to_right == True:                
                if distance > platform_x + 35: # go right
                    comm.send_instruction(scene_info.frame, PlatformAction.MOVE_RIGHT)
                elif distance < platform_x + 5: # go left
                    comm.send_instruction(scene_info.frame, PlatformAction.MOVE_LEFT)
                elif distance >= platform_x + 5 and distance <= platform_x + 35: # stop
                    comm.send_instruction(scene_info.frame, PlatformAction.NONE)                    
            elif bounce_to_left == True:          
                if 195 - distance > platform_x + 35: # go right
                    comm.send_instruction(scene_info.frame, PlatformAction.MOVE_RIGHT)
                elif 195 - distance < platform_x + 5: # go left
                    comm.send_instruction(scene_info.frame, PlatformAction.MOVE_LEFT)
                elif 195 - distance >= platform_x + 5 and distance <= platform_x + 35: # stop
                    comm.send_instruction(scene_info.frame, PlatformAction.NONE)
            
           

                

                

            

            
