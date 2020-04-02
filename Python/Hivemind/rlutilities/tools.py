def cap(x, low, high):
    return max(min(x, high), low)

def get_player_by_distance_to_target(data, index, target, team=None):
    """
    Gets a sorted list of distances from the players to the target,
    then returns the player that matches the indexed distance and team.

    data: Your preprocessed data class.
    index: Index of the sorted distance to target, 0 is the closest, 1 is second closest and so on.
    target: The target you are measuring the distances to.
    team: -1 or 1, you can input data.team to filter it to just your team or -data.team to filter it to the enemy team.
    """

    # Gets all players on the correct team.
    players = []
    for player in data.players:
        if team is None or player.team == team:
            players.append(player)

    # Gets a sorted list of distances to the target
    sorted_dists_to_target = sorted([player.distance_to_target_2d(target) for player in players])

    last = None
    for item in sorted_dists_to_target:
        if item == last:
            item += 1
        last = item

    # Goes through the players and returns the player that matches your index.
    if len(sorted_dists_to_target) >= index + 1:
        for player in players:
            if sorted_dists_to_target[index] == player.distance_to_target_2d(target):
                return player
    return None
