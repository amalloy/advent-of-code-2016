module Main where

import Day12.Parser (parseInstr)

main :: IO ()
main = interact $ unlines . map (show . parseInstr) . lines
