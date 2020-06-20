import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.scrollview import ScrollView
from random import randint

def rollx(number_of_dice, on_x_up, type_of_dice):
	number_of_successes = 0
	# first element of roll_array is a sub-array containing the number of successes
	# though unnecessary, the number_of_successes variable exists for readability purposes
	if type(number_of_dice)!="int" or type(on_x_up)!="int" or type(type_of_dice)!="int":
		#number_of_dice, on_x_up = 0,0
		roll_array=[[0],0]
	roll_array = [[number_of_successes]]
	for i in range(0,number_of_dice):
		roll = randint(1,type_of_dice)
		roll_array.append(roll)
		if roll >= on_x_up:
			 #number_of_successes+=1
			 roll_array[0][0] += 1
	return roll_array

class WrappedLabel(Label):
    # Based on Tshirtman's answer
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(
            width=lambda *x:
            self.setter('text_size')(self, (self.width, None)),
            texture_size=lambda *x: self.setter('height')(self, self.texture_size[1]))

class mainDiceRoller(GridLayout):
	def __init__(self, **kwargs):
		super(mainDiceRoller, self).__init__(**kwargs)

		####################
		# Logic Structure: #
		####################
		self.cols=1
		##
		self.inside = GridLayout(padding=[5,5,5,5])
		self.inside.cols=4
		##
		
		##
		self.button_array = GridLayout(padding=[0,0,5,0])
		self.button_array.cols=3
		##
		self.dice_state = 6

		self.d4_button = ToggleButton(text="d4", group="dice")
		self.d4_button.bind(on_press= lambda a: self.change_dice_state(N=4))

		# DEFAULT DICE STATE, WE PLAY 40K IN THIS HOUSE
		self.d6_button = ToggleButton(text="d6", group="dice", state="down")
		self.d6_button.bind(on_press= lambda a: self.change_dice_state(N=6))

		self.d8_button = ToggleButton(text="d8", group="dice")
		self.d8_button.bind(on_press= lambda a: self.change_dice_state(N=8))

		self.d10_button = ToggleButton(text="d10", group="dice")
		self.d10_button.bind(on_press= lambda a: self.change_dice_state(N=10))

		self.d12_button = ToggleButton(text="d12", group="dice")
		self.d12_button.bind(on_press= lambda a: self.change_dice_state(N=12))

		self.d20_button = ToggleButton(text="d20", group="dice")
		self.d20_button.bind(on_press= lambda a: self.change_dice_state(N=20))

		self.dN_button = ToggleButton(text="dN", group="dice")
		self.dN_input = TextInput(multiline=False, font_size=26)
		#dN_button setting dice_state is controlled under the do_roll method
		##

		self.xdx_grid = GridLayout(padding=[0,0,5,5], cols=1)
		##
		self.xdx_label = Label(text="Number of Dice to Roll:")
		self.xdx = TextInput(multiline=False, font_size=26)
		##
		self.xup_grid = GridLayout(padding=[0,0,5,5], cols=1)

		self.xup_label = Label(text="Succeeding on X+:")
		self.xup = TextInput(multiline=False, font_size=26)
		##


		##
		self.displayer = WrappedLabel(
			text="Roll array for "+"0"+" rolls:",
			halign="center",
			valign="center",
			font_size=20,
			padding=(0,0)
			)
		##
		self.roll_array_viewer = ScrollView()
		##
		self.roll_array_viewer_label = WrappedLabel(
			text="[ ]",
			halign="center",
			valign="center",
			font_size=18,
			size_hint_y=None,
			padding=(20,5)
			)
		##
		self.roll = Button(text="Roll", font_size=20)
		self.roll.bind(on_press=self.do_roll)


		#####################
		# DESIGN STRUCTURE: #
		#####################
		# structure of ButtonArray subwidget
		self.button_array.add_widget(self.d4_button)
		self.button_array.add_widget(self.d6_button)
		self.button_array.add_widget(self.d8_button)
		self.button_array.add_widget(self.d10_button)
		self.button_array.add_widget(self.d12_button)
		self.button_array.add_widget(self.d20_button)
		self.button_array.add_widget(self.dN_button)
		self.button_array.add_widget(self.dN_input)
		
		self.inside.add_widget(self.button_array)
		#
		self.xdx_grid.add_widget(self.xdx_label)
		self.xdx_grid.add_widget(self.xdx)
		self.xup_grid.add_widget(self.xup_label)
		self.xup_grid.add_widget(self.xup)
		self.inside.add_widget(self.xdx_grid)
		self.inside.add_widget(self.xup_grid)
		#
		self.add_widget(self.inside)
		self.add_widget(self.displayer)
		self.roll_array_viewer.add_widget(self.roll_array_viewer_label)
		self.add_widget(self.roll_array_viewer)
		self.add_widget(self.roll)

	####################
	# DECLARE METHODS: #
	####################
	def change_dice_state(self,N=6):
			self.dice_state = N

	def do_roll(self, event):
		#Handling events related to dN needing to be refreshed between rolls:
		if self.dN_button.state=="down":
			if self.dN_input.text=='':
				self.displayer.text="Please enter how many sides the die you are rolling is!"
				self.roll_array_viewer_label.text=""
				return None
			else:
				self.dice_state=int(self.dN_input.text)
		# Sanitize text inputs:
		XDX = "".join(self.xdx.text.split())
		XUP = "".join(self.xup.text.split())
		# Catch cases where no text is present in box:
		if XDX=="":
			XDX="1"
		if XUP=="":
			XUP="0"
		# Generate Roll Array:
		roll_ = rollx(int(XDX), int(XUP), self.dice_state)
		# Change displayed text according to whether a certain value must be rolled:
		if XUP == "0":
			self.displayer.text ="Roll array for "+XDX+" d"+str(self.dice_state)+" rolls:"
		else:
			self.displayer.text = "number of "+XUP+"+:\n "+str(roll_[0][0])+"\nRoll array for "+XDX+" d"+str(self.dice_state)+" rolls:"
		self.roll_array_viewer_label.text=str(roll_[1:])
		# Clear Roll Array:
		roll_=None

class DiceRoller(App):
	def build(self):
		return mainDiceRoller()

if __name__ == "__main__":
	DiceRoller().run()