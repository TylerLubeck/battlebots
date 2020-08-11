import Foundation

enum Hand : String, CaseIterable, Codable {
    case ROCK
    case PAPER
    case SCISSORS
}

struct Move : Codable {
    var move : Hand
    var art = ""

    func toJSON() throws -> String {
        let data = try JSONEncoder().encode(self)
        return String(data: data, encoding: .utf8)!
    }
}


