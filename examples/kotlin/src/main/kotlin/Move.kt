package battlebot

enum class Hand {
    ROCK,
    PAPER,
    SCISSORS
}

data class Move(val move: Hand, val art: String) {
    fun cheapJson(): String {
        return """
        |{"move": "${move}", "art": "${art}"}
        """.trimMargin("|")
    }
}
