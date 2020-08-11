package battlebot

import battlebot.Move
import battlebot.Hand

import kotlin.random.Random

class App {
    fun play_turn(history: List<String>) : Move {
        val hand = Hand.values().random()
        return Move(hand, emptyList())
    }
}
