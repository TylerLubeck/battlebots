package battlebot

import com.github.ajalt.clikt.core.CliktCommand
import com.github.ajalt.clikt.parameters.arguments.argument
import com.github.ajalt.clikt.parameters.arguments.default
import kotlin.system.exitProcess

import battlebot.App

class BattleBotCmd : CliktCommand() {
    val historyStr: String by argument(help="Game History").default("")

    override fun run() {
        try {
            val history = historyStr.split(";")
            val playerNumber = System.getenv("PLAYER_NUMBER") ?: "-"
            val move = App().play_turn(history, playerNumber)
            echo(move.toJSON())
        } catch (e: Exception) {
            exitProcess(1)
        }
    }
}

fun main(args: Array<String>) = BattleBotCmd().main(args)
