import pandas as pd
import re 

file_path = r"poker-data\poker_now_log_pglBfyNMj2pEPTAJ20tHZtQA5.csv"


# Read the CSV file using pandas
df = pd.read_csv(file_path)



groupMap = {}

currentPlayersSet = set()
currentPlayersTuple = ()
joinPattern =  r'"([^"]+)"\s+(joined the game|sit back)'
leavePattern = r'player\s"(\w+)\s@.*stand\sup'
playerNameUsingStacksPattern = r'"([^"]+@[^"]+)"'
tracking_hand = False


grouped_df = []
current_group = []

for index, row in df[::-1].iterrows():
    entry = row['entry']
    
    if "-- starting hand" in entry:
        if current_group:  
            grouped_df.append(current_group)
        current_group = [] 
    else:
        current_group.append(entry)


for hand in grouped_df: 
    currentPlayersTuple = ()
    for action in hand:
        entry = action
        if "Flop:" in entry:
            break
        if "Player stacks:" in entry:
            playerNameMatch = re.findall(playerNameUsingStacksPattern, entry)
            currentPlayersTuple = tuple(sorted([match.split(" @ ")[0] for match in playerNameMatch]))
            groupMap[currentPlayersTuple] = groupMap.get(currentPlayersTuple, {})
            groupMap[currentPlayersTuple]['totalHandsPlayedByGroup'] = groupMap[currentPlayersTuple].get('totalHandsPlayedByGroup', 0) + 1
        if "raises to" in entry or "calls" in entry:
            player_name = entry.split(' @ ')[0].replace('"', '')
            currentGroupMap = groupMap.get(currentPlayersTuple, {})
            currentGroupMap[player_name] = currentGroupMap.get(player_name, 0) + 1
            groupMap[currentPlayersTuple] = currentGroupMap
# Output the results
# print(groupMap)


#vpip 

handsPlayedMap = {}

for group, groupParticipation in groupMap.items():
    handsPlayedByAll = 0
    for player, playedHandsCount in groupParticipation.items():
        handsPlayedMap[player] = handsPlayedMap.get(player, {})
        handsPlayedMap[player]['handsPlayedByPlayer'] = handsPlayedMap[player].get('handsPlayedByPlayer', 0) + playedHandsCount
        handsPlayedByAll += playedHandsCount 
    for player, playedHandsCount in groupParticipation.items():
        handsPlayedMap[player]['handsPlayedByAll'] = handsPlayedMap[player].get('handsPlayedByAll', 0) + groupParticipation['totalHandsPlayedByGroup']
for player, stats in handsPlayedMap.items():
  # Skip total group data
    hands_played_by_player = stats['handsPlayedByPlayer']
    hands_played_by_all = stats['handsPlayedByAll']
    percentage = (hands_played_by_player / hands_played_by_all) * 100
    print(f"{player}:")
    print(f"  Hands Played by Player: {hands_played_by_player}")
    print(f"  Hands Played by People They Played With: {hands_played_by_all}")
    print(f"  Percentage: {percentage:.2f}%\n")
    
        