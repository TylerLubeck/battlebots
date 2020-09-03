func play_turn(history: [String], playerNumber: String) -> Move {
    var art : [String] = []
    if playerNumber == "1" {
        art = ["*"]
    } else if playerNumber == "2" {
        art = ["**"]
    }

    return Move(
        move: Hand.allCases.randomElement()!,
        art: art
    )
}
