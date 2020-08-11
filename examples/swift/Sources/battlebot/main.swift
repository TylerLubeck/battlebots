import ArgumentParser
import Foundation

struct BattleBot: ParsableCommand {
    static let configuration = CommandConfiguration(abstract: "A BattleBot Implementation")

    @Argument(help: "Game History")
    private var history: String = ""

    func run() throws {
        let history_array = history.components(separatedBy: ";").filter({ !$0.isEmpty})
        do {
            let move = play_turn(history: history_array)
            let s = try move.toJSON()
            print(s)
        } catch {
            throw ExitCode.failure
        }
    }
}

BattleBot.main()
