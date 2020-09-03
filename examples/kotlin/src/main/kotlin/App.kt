package battlebot

import battlebot.Move
import battlebot.Hand

import kotlin.random.Random

class App {
    fun play_turn(history: List<String>, playerNumber: String) : Move {
        var art = listOf<String>()
        
        if (playerNumber == "1") {
            art = listOf("*")
        } else if (playerNumber == "2") {
            art = listOf("**")
        }
        val hand = Hand.values().random()
        return Move(hand, art)
    }
}
