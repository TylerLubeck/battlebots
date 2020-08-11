# Example Swift Battlebot

This directory holds a sample Rock-Paper-Scissors bot written in Swift. It always plays a random hand.

## To Implement

Implement the function `Sources/battlebot/app.swift::play_turn`

## To Build

Run `make image`

## To Test

You can perform a basic manual test by running `make run`.

You can perform manual tests with a history by running `make run-with-history`. If you want to provide your own history,
either edit the `Makefile` or run `HISTORY="rp2;ss1;ss2;" make run-with-history`.
