import tkinter as tk
from tkinter import messagebox
import random

class DinosaurGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Dinosaur Jump Game")
        self.root.resizable(False, False)
        self.root.config(bg="#f7f7f7")
        
        # Game variables
        self.game_running = False
        self.score = 0
        self.high_score = 0
        self.is_jumping = False
        self.jump_count = 0
        self.max_jump = 15
        self.gravity = 1
        self.obstacle_speed = 8
        self.obstacles = []
        self.game_speed_increment = 0
        
        # Create main frame
        main_frame = tk.Frame(root, bg="#f7f7f7")
        main_frame.pack(padx=20, pady=20)
        
        # Title
        title_label = tk.Label(
            main_frame,
            text="🦖 Dinosaur Jump Game",
            font=("Helvetica", 24, "bold"),
            bg="#f7f7f7",
            fg="#535353"
        )
        title_label.pack(pady=10)
        
        # Score Frame
        score_frame = tk.Frame(main_frame, bg="#f7f7f7")
        score_frame.pack(pady=5)
        
        self.score_label = tk.Label(
            score_frame,
            text="Score: 0",
            font=("Helvetica", 14),
            bg="#f7f7f7",
            fg="#535353"
        )
        self.score_label.pack(side=tk.LEFT, padx=10)
        
        self.high_score_label = tk.Label(
            score_frame,
            text="High Score: 0",
            font=("Helvetica", 14),
            bg="#f7f7f7",
            fg="#535353"
        )
        self.high_score_label.pack(side=tk.LEFT, padx=10)
        
        # Canvas for game
        self.canvas = tk.Canvas(
            main_frame,
            width=800,
            height=300,
            bg="#f7f7f7",
            highlightthickness=2,
            highlightbackground="#535353"
        )
        self.canvas.pack(pady=10)
        
        # Draw ground
        self.ground_y = 250
        self.canvas.create_line(0, self.ground_y, 800, self.ground_y, fill="#535353", width=2)
        
        # Create dinosaur
        self.dino_x = 100
        self.dino_y = self.ground_y - 40
        self.dino_width = 40
        self.dino_height = 40
        
        self.dinosaur = self.canvas.create_rectangle(
            self.dino_x,
            self.dino_y,
            self.dino_x + self.dino_width,
            self.dino_y + self.dino_height,
            fill="#535353",
            outline="#535353"
        )
        
        # Add dinosaur details (head)
        self.dino_head = self.canvas.create_rectangle(
            self.dino_x + 25,
            self.dino_y - 10,
            self.dino_x + 40,
            self.dino_y + 10,
            fill="#535353",
            outline="#535353"
        )
        
        # Add eye
        self.dino_eye = self.canvas.create_oval(
            self.dino_x + 30,
            self.dino_y - 5,
            self.dino_x + 35,
            self.dino_y,
            fill="white",
            outline="white"
        )
        
        # Buttons Frame
        button_frame = tk.Frame(main_frame, bg="#f7f7f7")
        button_frame.pack(pady=10)
        
        self.start_button = tk.Button(
            button_frame,
            text="Start Game",
            font=("Helvetica", 12, "bold"),
            bg="#4CAF50",
            fg="white",
            width=12,
            command=self.start_game,
            cursor="hand2"
        )
        self.start_button.pack(side=tk.LEFT, padx=5)
        
        self.stop_button = tk.Button(
            button_frame,
            text="Stop Game",
            font=("Helvetica", 12, "bold"),
            bg="#f44336",
            fg="white",
            width=12,
            state="disabled",
            command=self.stop_game,
            cursor="hand2"
        )
        self.stop_button.pack(side=tk.LEFT, padx=5)
        
        self.restart_button = tk.Button(
            button_frame,
            text="Restart",
            font=("Helvetica", 12, "bold"),
            bg="#2196F3",
            fg="white",
            width=12,
            command=self.restart_game,
            cursor="hand2"
        )
        self.restart_button.pack(side=tk.LEFT, padx=5)
        
        # Instructions
        instructions = tk.Label(
            main_frame,
            text="Press SPACE or UP ARROW to Jump | Avoid the obstacles!",
            font=("Helvetica", 10),
            bg="#f7f7f7",
            fg="#888888"
        )
        instructions.pack(pady=5)
        
        # Bind keys
        self.root.bind("<space>", lambda e: self.jump())
        self.root.bind("<Up>", lambda e: self.jump())
        
    def start_game(self):
        """Start the game"""
        if not self.game_running:
            self.game_running = True
            self.start_button.config(state="disabled")
            self.stop_button.config(state="normal")
            self.game_loop()
            self.spawn_obstacles()
    
    def stop_game(self):
        """Stop the game"""
        self.game_running = False
        self.start_button.config(state="normal")
        self.stop_button.config(state="disabled")
        
        # Update high score
        if self.score > self.high_score:
            self.high_score = self.score
            self.high_score_label.config(text=f"High Score: {self.high_score}")
        
        messagebox.showinfo("Game Stopped", f"Game Over!\nFinal Score: {self.score}")
    
    def restart_game(self):
        """Restart the game"""
        # Stop current game
        self.game_running = False
        
        # Clear obstacles
        for obstacle in self.obstacles:
            self.canvas.delete(obstacle['rect'])
        self.obstacles.clear()
        
        # Reset variables
        self.score = 0
        self.is_jumping = False
        self.jump_count = 0
        self.obstacle_speed = 8
        self.game_speed_increment = 0
        
        # Reset dinosaur position
        self.dino_y = self.ground_y - 40
        self.canvas.coords(
            self.dinosaur,
            self.dino_x,
            self.dino_y,
            self.dino_x + self.dino_width,
            self.dino_y + self.dino_height
        )
        self.canvas.coords(
            self.dino_head,
            self.dino_x + 25,
            self.dino_y - 10,
            self.dino_x + 40,
            self.dino_y + 10
        )
        self.canvas.coords(
            self.dino_eye,
            self.dino_x + 30,
            self.dino_y - 5,
            self.dino_x + 35,
            self.dino_y
        )
        
        # Update score
        self.score_label.config(text="Score: 0")
        
        # Enable start button
        self.start_button.config(state="normal")
        self.stop_button.config(state="disabled")
    
    def jump(self):
        """Make the dinosaur jump"""
        if not self.is_jumping and self.game_running:
            self.is_jumping = True
            self.jump_count = 0
    
    def update_jump(self):
        """Update jumping animation"""
        if self.is_jumping:
            if self.jump_count < self.max_jump:
                # Move up
                move_y = -10
                self.jump_count += 1
            else:
                # Move down
                move_y = 10
                if self.dino_y >= self.ground_y - 40:
                    # Landed
                    self.is_jumping = False
                    self.jump_count = 0
                    # Correct position
                    self.dino_y = self.ground_y - 40
                    self.canvas.coords(
                        self.dinosaur,
                        self.dino_x,
                        self.dino_y,
                        self.dino_x + self.dino_width,
                        self.dino_y + self.dino_height
                    )
                    self.canvas.coords(
                        self.dino_head,
                        self.dino_x + 25,
                        self.dino_y - 10,
                        self.dino_x + 40,
                        self.dino_y + 10
                    )
                    self.canvas.coords(
                        self.dino_eye,
                        self.dino_x + 30,
                        self.dino_y - 5,
                        self.dino_x + 35,
                        self.dino_y
                    )
                    return
            
            self.dino_y += move_y
            self.canvas.move(self.dinosaur, 0, move_y)
            self.canvas.move(self.dino_head, 0, move_y)
            self.canvas.move(self.dino_eye, 0, move_y)
    
    def spawn_obstacles(self):
        """Spawn obstacles"""
        if self.game_running:
            # Random obstacle type
            obstacle_type = random.choice(['cactus', 'bird'])
            
            if obstacle_type == 'cactus':
                # Create cactus obstacle
                obstacle_width = random.choice([20, 30, 40])
                obstacle_height = random.choice([40, 50, 60])
                obstacle_x = 800
                obstacle_y = self.ground_y - obstacle_height
                
                obstacle_rect = self.canvas.create_rectangle(
                    obstacle_x,
                    obstacle_y,
                    obstacle_x + obstacle_width,
                    obstacle_y + obstacle_height,
                    fill="#2d7a2d",
                    outline="#2d7a2d"
                )
            else:
                # Create bird obstacle
                obstacle_width = 40
                obstacle_height = 30
                obstacle_x = 800
                obstacle_y = random.choice([self.ground_y - 100, self.ground_y - 60])
                
                obstacle_rect = self.canvas.create_oval(
                    obstacle_x,
                    obstacle_y,
                    obstacle_x + obstacle_width,
                    obstacle_y + obstacle_height,
                    fill="#8B4513",
                    outline="#8B4513"
                )
            
            self.obstacles.append({
                'rect': obstacle_rect,
                'x': obstacle_x,
                'width': obstacle_width
            })
            
            # Spawn next obstacle after random delay
            next_spawn = random.randint(1500, 3000)
            self.root.after(next_spawn, self.spawn_obstacles)
    
    def move_obstacles(self):
        """Move obstacles from right to left"""
        for obstacle in self.obstacles[:]:
            # Move obstacle
            obstacle['x'] -= self.obstacle_speed
            self.canvas.coords(
                obstacle['rect'],
                obstacle['x'],
                self.canvas.coords(obstacle['rect'])[1],
                obstacle['x'] + obstacle['width'],
                self.canvas.coords(obstacle['rect'])[3]
            )
            
            # Remove obstacle if it's off screen
            if obstacle['x'] + obstacle['width'] < 0:
                self.canvas.delete(obstacle['rect'])
                self.obstacles.remove(obstacle)
                
                # Increase score
                self.score += 10
                self.score_label.config(text=f"Score: {self.score}")
                
                # Increase difficulty every 50 points
                if self.score % 50 == 0:
                    self.obstacle_speed += 1
    
    def check_collision(self):
        """Check if dinosaur collides with obstacle"""
        dino_coords = self.canvas.coords(self.dinosaur)
        dino_head_coords = self.canvas.coords(self.dino_head)
        
        for obstacle in self.obstacles:
            obs_coords = self.canvas.coords(obstacle['rect'])
            
            # Check collision with body
            if (dino_coords[2] > obs_coords[0] and 
                dino_coords[0] < obs_coords[2] and 
                dino_coords[3] > obs_coords[1] and 
                dino_coords[1] < obs_coords[3]):
                return True
            
            # Check collision with head
            if (dino_head_coords[2] > obs_coords[0] and 
                dino_head_coords[0] < obs_coords[2] and 
                dino_head_coords[3] > obs_coords[1] and 
                dino_head_coords[1] < obs_coords[3]):
                return True
        
        return False
    
    def game_loop(self):
        """Main game loop"""
        if self.game_running:
            # Update jump
            self.update_jump()
            
            # Move obstacles
            self.move_obstacles()
            
            # Check collision (optional: you can remove this if you don't want collision detection)
            # if self.check_collision():
            #     self.stop_game()
            #     return
            
            # Continue loop
            self.root.after(30, self.game_loop)

# Create and run the game
if __name__ == "__main__":
    root = tk.Tk()
    game = DinosaurGame(root)
    root.mainloop()