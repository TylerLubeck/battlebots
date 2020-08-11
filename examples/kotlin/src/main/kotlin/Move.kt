package battlebot

import com.google.gson.Gson

enum class Hand {
    ROCK,
    PAPER,
    SCISSORS
}

data class Move(val move: Hand, val art: List<String> = emptyList()) {
    fun toJSON(): String {
        return Gson().toJson(this)
    }
}
