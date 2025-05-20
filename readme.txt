Usage: python3 chessmain.py <mode: 0|1> <firstTurn: 0|1> <whiteLevel: 1-10> <blackLevel: 1-5>
<mode>: interger
1: agent vs random agent
0: agent vs agent
<whiteLevel>: 1-5 level of agentWhite
<blackLevel>: 1-5 level of agentBlack

<first-turn>: interger if agent vs agent: firstTurn is not importTant (firstTurn is always for white)
if radomAI vs agent:  
<first-turn == 1 >: radomAI is black and whileLevel is level for agent (blackLevel is not important) example: 1 1 3 0 (3 is level of agent) 
<first-turn == 0 >: radomAI is white and blackLevel is level for agent (whiteLevel is not important) example: 1 0 0 3 (3 is level of agent) 
