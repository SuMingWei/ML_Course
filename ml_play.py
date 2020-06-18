class MLPlay:
    def __init__(self, player):
        self.player = player
        if self.player == "player1":
            self.player_no = 0
        elif self.player == "player2":
            self.player_no = 1
        elif self.player == "player3":
            self.player_no = 2
        elif self.player == "player4":
            self.player_no = 3
        self.car_vel = 0
        self.car_pos = (0,0)

        self.moving = False
        self.line = self.car_pos[0] // 70
        self.action = "none"
        pass
    
    def update(self, scene_info):
        """
        Generate the command according to the received scene information
        """

        max_speed = self.car_vel
        nearest_dis = 10000     
        close = False   

        left_min_speed = self.car_vel
        left_near_dis = 10000
        left_max_speed = self.car_vel
        left_front_near_dis = 10000

        right_min_speed = self.car_vel
        right_near_dis = 10000
        right_max_speed = self.car_vel
        right_front_near_dis = 10000

        left_num = 0
        right_num = 0
        front_num = 0

        left_has_car = False
        left_behind_has_car = False
        right_has_car = False
        right_behind_has_car = False

        brake = False
        left = False
        right = False        

        grid = set()

        if len(scene_info[self.player]) != 0:
            self.car_pos = scene_info[self.player]                    

        for car in scene_info["cars_info"]:
            if car["id"] == self.player_no:
                self.car_vel = car["velocity"]               
                
                if(self.moving == False):
                    if(0 <= self.car_pos[0]) and (self.car_pos[0] <= 90):
                        current_line = 0
                    elif(90 < self.car_pos[0]) and (self.car_pos[0] <= 160):              
                        current_line = 1
                    elif(160 < self.car_pos[0]) and (self.car_pos[0] <= 230):              
                        current_line = 2
                    elif(230 < self.car_pos[0]) and (self.car_pos[0] <= 300):              
                        current_line = 3
                    elif(300 < self.car_pos[0]) and (self.car_pos[0] <= 370):              
                        current_line = 4
                    elif(370 < self.car_pos[0]) and (self.car_pos[0] <= 440):              
                        current_line = 5
                    elif(440 < self.car_pos[0]) and (self.car_pos[0] <= 510):              
                        current_line = 6
                    elif(510 < self.car_pos[0]) and (self.car_pos[0] <= 580):              
                        current_line = 7
                    elif(580 < self.car_pos[0]) and (self.car_pos[0] <= 650):              
                        current_line = 8                    
                    
                    self.line = current_line
                
            elif (car["id"] != self.player_no) and (self.moving == False):     
                lane = car["pos"][0] // 70 # car lane
                #front has car                
                if (lane == self.line) and (car["pos"][1] < self.car_pos[1]):
                #if (car["pos"][0] <= self.line * 70 + 75)and(car["pos"][0] >= self.line * 70 - 5) and (car["pos"][1] < self.car_pos[1]):
                #if (car["pos"][0] == self.line * 70 + 35) and (car["pos"][1] < self.car_pos[1]):
                    front_num += 1
                    temp_dis = self.car_pos[1] - car["pos"][1]
                    if(temp_dis < nearest_dis):
                        nearest_dis = temp_dis
                        max_speed = car["velocity"]                  
                #left has car                
                if (self.line > 0) and (lane == self.line - 1):
                #if (self.line > 0) and (car["pos"][0] <= (self.line - 1)* 70 + 75) and (car["pos"][0] >= (self.line - 1)* 70 + 5):
                #if (self.line > 0) and (car["pos"][0] == (self.line - 1)* 70 + 35):
                    # left side has car
                    if (car["pos"][1] >= self.car_pos[1] - 160) and (car["pos"][1] <= self.car_pos[1] + 100):
                        # left front car number
                        if(car["pos"][1] >= self.car_pos[1] - 160):
                            left_num += 1
                        left_has_car = True
                    else:                                                
                        # left behind car speed
                        temp_dis = car["pos"][1] - (self.car_pos[1] + 80)
                        if(temp_dis > 20) and (temp_dis <= 120):
                            left_behind_has_car = True    
                        if (temp_dis < left_near_dis) and (temp_dis >= 0):
                            left_near_dis = temp_dis
                            left_min_speed = car["velocity"]
                        # left front car speed
                        temp_dis = self.car_pos[1] - car["pos"][1]
                        if(temp_dis < left_front_near_dis) and (temp_dis >= 0):
                            left_front_near_dis = temp_dis
                            left_max_speed = car["velocity"]                
                #right has car                
                if (self.line < 8) and (lane == self.line + 1):
                #if (self.line < 8) and (car["pos"][0] <= (self.line + 1)* 70 + 75) and (car["pos"][0] >= (self.line + 1)* 70 + 5):
                #if (self.line < 8) and (car["pos"][0] == (self.line + 1)* 70 + 35):
                    #right side has car
                    if(car["pos"][1] >= self.car_pos[1] - 160) and (car["pos"][1] <= self.car_pos[1] + 100):
                        # right front car number
                        if(car["pos"][1] >= self.car_pos[1] - 160):
                            right_num += 1
                        right_has_car = True
                    else:                     
                        # right behind car speed
                        temp_dis = car["pos"][1] - (self.car_pos[1] + 80) 
                        if(temp_dis > 20) and (temp_dis <= 120):
                            right_behind_has_car = True
                        if(temp_dis < right_near_dis) and (temp_dis >= 0):
                            right_near_dis = temp_dis
                            right_min_speed = car["velocity"]  
                        # right front car speed
                        temp_dis = self.car_pos[1] - car["pos"][1]
                        if(temp_dis < right_front_near_dis) and (temp_dis >= 0):
                            right_front_near_dis = temp_dis
                            right_max_speed = car["velocity"]  
                                
            #change to left or right
            if(self.moving == True):                
                if(self.action == "left") and (self.car_pos[0] != (self.line - 1) * 70 + 35): 
                    if(self.car_vel > max_speed) and (front_num >= 2):                        
                        return ["BRAKE" , "MOVE_LEFT"]
                    else:                         
                        return ["SPEED", "MOVE_LEFT"]                
                elif(self.action == "right") and (self.car_pos[0] != (self.line + 1) * 70 + 35):                    
                    if(self.car_vel > max_speed) and (front_num >= 2):                        
                        return ["BRAKE" , "MOVE_RIGHT"]
                    else:
                        return ["SPEED", "MOVE_RIGHT"]            
                else:                
                    if(self.action == "left"):
                        self.line -= 1
                    elif (self.action == "right"):
                        self.line += 1
                    self.action = "none"
                    self.moving = False                    
                    print("now",self.line,self.moving)
                    return ["SPEED"] 

            if(left_has_car):
                grid.add(1)
            if(nearest_dis != 10000):
                grid.add(2)
            if(right_has_car):
                grid.add(3)
            if(left_behind_has_car):
                grid.add(7)
            if(right_behind_has_car):
                grid.add(9)
            print(grid)       

        if(nearest_dis <= 280): 
            #front car very close
            if(nearest_dis <=200):
                close = True
            else:
                close = False
            # turn to the line that has least car    
            if left_num < right_num:
                #can change to left
                if(self.line != 0) and (left_has_car == False) and (self.car_vel < left_max_speed):                    
                    self.moving = True
                    self.action = "left"
                    left = True
                else:
                    brake = False
                    left = False
                #can change to right
                if(self.line != 8) and (right_has_car == False) and (left == False) and (self.car_vel < right_max_speed):            
                    self.moving = True
                    self.action = "right"
                    right = True
                else:
                    brake = False
                    right = False
            elif (left_num > right_num):
                #can change to right
                if(self.line != 8) and (right_has_car == False) and (self.car_vel < right_max_speed):                    
                    self.moving = True
                    self.action = "right"
                    right = True
                else:
                    brake = False
                    right = False
                #can change to left
                if(self.line != 0) and (left_has_car == False) and (right == False) and (self.car_vel < left_max_speed):            
                    self.moving = True
                    self.action = "left"
                    left = True
                else:
                    brake = False
                    left = False   
            elif(left_num == right_num):
                if(self.line < 5):
                    #can change to right
                    if(self.line != 8) and (right_has_car == False) and (self.car_vel < right_max_speed):                    
                        self.moving = True
                        self.action = "right"
                        right = True
                    else:
                        brake = False
                        right = False
                    #can change to left
                    if(self.line != 0) and (left_has_car == False) and (right == False) and (self.car_vel < left_max_speed):            
                        self.moving = True
                        self.action = "left"
                        left = True
                    else:
                        brake = False
                        left = False  
                elif(self.line >= 5): 
                    #can change to left
                    if(self.line != 0) and (left_has_car == False) and (self.car_vel < left_max_speed):                    
                        self.moving = True
                        self.action = "left"
                        left = True
                    else:
                        brake = False
                        left = False
                    #can change to right
                    if(self.line != 8) and (right_has_car == False) and (left == False) and (self.car_vel < right_max_speed):            
                        self.moving = True
                        self.action = "right"
                        right = True
                    else:
                        brake = False
                        right = False
            #must keep in line
            if(left == False) and (right == False) and (self.car_vel > max_speed):
                self.moving = False
                self.action = "none"
                brake = True
        else:
            #forward
            brake = False 

        if brake == True:                                
            return ["BRAKE"]
        elif brake == False:
            if(close == False):            
                if(left == True):                
                    return ["SPEED", "MOVE_LEFT"]
                elif(right == True):                
                    return ["SPEED", "MOVE_RIGHT"]
                else:
                    return["SPEED"]
                    
            elif (close == True):
                if front_num >= 2:
                    return["BRAKE"]
                
                if (left_behind_has_car == False) and (left == True):
                    if self.car_vel <= max_speed:
                        return ["SPEED", "MOVE_LEFT"]
                    else:
                        return ["BRAKE", "MOVE_LEFT"]
                elif (right_behind_has_car == False) and (right == True):
                    if self.car_vel <= max_speed:
                        return ["SPEED", "MOVE_RIGHT"]
                    else:
                        return ["BRAKE", "MOVE_RIGHT"]
                else:
                    if self.car_vel < max_speed: 
                        return ["SPEED"]
                    else:
                        return ["BRAKE"]
                
        if scene_info["status"] != "ALIVE":
            return "RESET"        


    def reset(self):
        """
        Reset the status
        """
        pass
