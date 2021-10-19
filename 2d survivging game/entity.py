import itemIds
import CharacterFile
import pygame

class Entity():
	yVelocity = 0
	xVelocity = 0

	def __init__(self,worldCoordinates,size,index,id):
		self.drawCoordinates = [worldCoordinates[0]/32,worldCoordinates[1]/32]
		self.coordinates = worldCoordinates

		self.boundingBox = pygame.Rect(self.drawCoordinates,size)
		self.index = index
		self.id = id
		self.texture = itemIds.Items.iconList[self.id]
	
	def update(self):
		
		self.drawCoordinates[0] = self.coordinates[0]*32 - CharacterFile.Character.characterLocation[0]*32
		self.drawCoordinates[1] = self.coordinates[1]*32 - CharacterFile.Character.characterLocation[1]*32
	def gravityUpdate(self,terminalVelocity = 10,gravity = 5):
		if self.boundingBox[1] < 200:
			self.yVelocity += gravity
		if self.yVelocity > terminalVelocity:
			self.yVelocity = terminalVelocity
		if self.boundingBox[1] >= 180:
			self.yVelocity = 0
		self.boundingBox[1] += self.yVelocity


	def deleteEntity(self,index):
		if self.index < index:
			return False
		elif self.index > index:
			self.index -= 1
			return False
		else:
			return True

frameNumber = 0
entities = []
hue = 0

def delete(index):
	if len(entities) > index:
		if len(entities) > 0:
			entities[index].deleteEntity(index)
		del entities[index]
		print(len(entities))


	"""
	delete funciton can be run whenever i want to get rid of an entity. i can use a for loop to iterate through the list of entites and check for colisisions with an item pickup hitbox and if the collision returns true then i can add an item with that id and quantity to the players inventory then run the delete function on the entity.
	"""
