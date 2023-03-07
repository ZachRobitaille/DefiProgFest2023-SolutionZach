# Explication du code de la fonction get_action()
La solution a premièrement été faite pour les trois premiers échelons en continu. En fonction des réponses en continu, les actions en discret ont pu plus facilement être déterminées.

Aucune équation mathématique a été utilisé. Seulement du gros bon sens.

Plus le lander chute rapidement, plus le moteur central sera puissant. Si le lander est penché, un moteur latéral sera activé. Cependant, si le lander est penché et que la vitesse angulaire favorise le retour à l'équilibre, la puisance du moteur latéral sera modéré. 

Plus le lander est décalé vers l'un des coté, plus un des moteur latéral sera puissant. Cependant, si la vitesse du lander est favorable au retour au centre, la puissance du moteur latéral sera changé, voir changé pour l'autre moteur latéral.

Finalement, plus le lander est près du sol, plus le moteur central sera puissant pour assurer un atterissage en douceur.