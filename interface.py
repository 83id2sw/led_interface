import customtkinter
import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM) #выбор другой нумерации выводов
GPIO.setup(6, GPIO.OUT) #green led
GPIO.setup(5, GPIO.OUT) #blue led
GPIO.setup(8, GPIO.OUT) #red led

pwmRed = GPIO.PWM(8, 500)
pwmRed.start(0)

pwmGreen = GPIO.PWM(6, 500)
pwmGreen.start(0)

pwmBlue = GPIO.PWM(5, 500)
pwmBlue.start(0)

customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("green")  # Themes: "blue" (standard), "green", "dark-blue"


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("RGB LED Control")
        self.geometry(f"{800}x{380}")

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="RGB LED Control",
                                                 font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame,
                                                                       values=["Dark", "Light", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))
        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame,
                                                               values=["80%", "90%", "100%", "110%", "120%"],
                                                               command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20))

        # create slider and progressbar frame
        self.slider_progressbar_frame = customtkinter.CTkFrame(self, fg_color="transparent")
        self.slider_progressbar_frame.grid(row=1, column=1, columnspan=2, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.slider_progressbar_frame.grid_columnconfigure(0, weight=1)
        self.slider_progressbar_frame.grid_rowconfigure(4, weight=1)
        self.slider_red = customtkinter.CTkSlider(self.slider_progressbar_frame, from_=0, to=100, command=self.updateRed)
        self.slider_red.grid(row=1, column=1, padx=(20, 10), pady=(10, 10), sticky="ew")
        self.slider_green = customtkinter.CTkSlider(self.slider_progressbar_frame, from_=0, to=100, command=self.updateGreen)
        self.slider_green.grid(row=2, column=1, padx=(20, 10), pady=(10, 10), sticky="ew")
        self.slider_blue = customtkinter.CTkSlider(self.slider_progressbar_frame, from_=0, to=100, command=self.updateBlue)
        self.slider_blue.grid(row=3, column=1, padx=(20, 10), pady=(10, 10), sticky="ew")

        # label
        self.label_red = customtkinter.CTkLabel(self.slider_progressbar_frame, text="Red (0-255):", text_color="Red")
        self.label_red.grid(row=1, column=0)
        self.label_red = customtkinter.CTkLabel(self.slider_progressbar_frame, text="Green (0-255):", text_color="Green")
        self.label_red.grid(row=2, column=0)
        self.label_red = customtkinter.CTkLabel(self.slider_progressbar_frame, text="Blue (0-255):", text_color="Blue")
        self.label_red.grid(row=3, column=0, padx=20, pady=(10, 0))

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def updateRed(self, duty):
        pwmRed.ChangeDutyCycle(float(duty))

    def updateGreen(self, duty):
        pwmGreen.ChangeDutyCycle(float(duty))

    def updateBlue(self, duty):
        pwmBlue.ChangeDutyCycle(float(duty))


if __name__ == "__main__":
    app = App()
    app.mainloop()
