func play_turn(history: [String]) -> Move {
    return Move(
        move: Hand.allCases.randomElement()!,
        art: ""
    )
}
