from copy import deepcopy
from typing import Union

import gym
import numpy as np

from tools.env_config_formatter import convert_str_attr_to_float_env_config


class LunarLanderAgent:
	"""
	Class LunarLanderAgent. Vous devez modifier cette classe pour que votre agent puisse apprendre à jouer à LunarLander.
	
	Attributes:
		env_config (dict): Dictionnaire contenant les paramètres de l'environnement.
		observation_as_rgb (bool): True si l'environnement est configuré pour retourner des observations sous forme
			d'images.
	"""
	def __init__(self, env_config: dict, **kwargs):
		"""
		Constructor de la classe LunarLanderAgent.
		
		:param env_config: Dictionnaire contenant les paramètres de l'environnement.
		:type env_config: dict
		:param kwargs: Arguments optionnels.
		"""
		self.env_config = env_config
		self.set_default_env_config()
		self.observation_as_rgb = self.env_config.get("render_mode", None) == "rgb_array"
	
	def set_default_env_config(self):
		self.env_config.setdefault('render_mode', None)
		self.env_config.setdefault('id', "LunarLander-v2")
	
	def make_env(self, env_config: dict = None):
		"""
		Cette classe est utilisée pour créer un environnement avec les paramètres de self.env_config.

		Note: L'agent n'interagie pas avec cet environnement. Celui-ci est seulement utilisé pour récupérer des
			informations sur l'environnement comme l'espace d'actions et l'espace d'observations. Il peut aussi être
			utilisé pour tester l'agent.

		:return: Un environnement avec les paramètres de self.env_config.
		:rtype: gym.Env
		"""
		if env_config is None:
			env_config = self.env_config
		env_config = convert_str_attr_to_float_env_config(env_config)
		env = gym.make(**env_config)
		return env
	
	def get_action(self, observation: np.ndarray) -> Union[int, np.ndarray]:
		"""
		Cette méthode est utilisée pour récupérer une action à partir d'une observation.
		
		:param observation: Observation de l'environnement.
		:type observation: np.ndarray
		:return: Action à effectuer dans l'environnement.
		:rtype: Union[int, np.ndarray]
		"""
		# État du lander x: position horizontale  xv: vitesse horizontale
		x, y, xv, yv, theta, omega = observation[0], observation[1], observation[2], observation[3], observation[4], observation[5]
		# Initialisation de l'état des moteurs
		yBooster = 0.
		xBooster = 0.

		# Si le lander n'est toujours pas atterri
		if observation[6] == False or observation[7] == False:
			#Dealing with height
			if yv < 0:
				yBooster = np.abs(yv) - (y/7 if y > 0.10 else -0.10)
		#Dealing with orientation
		xBooster = np.sin(theta)*2.5 + omega*2.5
		
		#Dealing with x position and velocity
		xBooster -= x*3 + xv*4


		env = self.make_env()
		env.close()

		action = np.array([yBooster,xBooster])
		if self.env_config['continuous']:
			return action
		else:
			#Trust me bro
			if action[0]  > np.abs(action[1]):
				return 2
			if y < 0.05:
				return 2 if yv < -0.1 else 0
			else:
				if action[1] < -0.5: return 1
				elif action[1] > 0.5: return 3
				else: 
					if yv > -0.08 and y > 0.15:
						return 0 
					else:
						return 2 if yv < -0.1 else 0
		
	def visualise_trajectory(self, seed=None) -> float:
		"""
		Cette méthode est utilisée pour visualiser une trajectoire de l'agent.

		:param seed: Seed pour l'environnement.

		:return: Cumulative reward de la trajectoire.
		"""
		viz_env_config = deepcopy(self.env_config)
		viz_env_config["render_mode"] = "human"
		env = self.make_env(viz_env_config)
		observation, info = env.reset(seed=seed)
		terminal = False
		cumulative_rewards = 0.0
		while not terminal:
			if self.observation_as_rgb:
				rgb_observation = env.render()
				action = self.get_action(rgb_observation)
			else:
				action = self.get_action(observation)
			observation, reward, done, truncated, info = env.step(action)
			cumulative_rewards += reward
			terminal = done or truncated
		return cumulative_rewards


if __name__ == '__main__':
	import json
	
	configs = json.load(open(f"./env_configs.json", "r"))
	echelon_id: int = 2
	echelon_key = [key for key in configs.keys() if key.startswith(f"Echelon {echelon_id}")][0]
	agent = LunarLanderAgent(configs[echelon_key])
	cr = agent.visualise_trajectory()
	print(f"Cumulative reward: {cr:.2f}")

