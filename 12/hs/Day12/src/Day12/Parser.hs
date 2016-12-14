module Day12.Parser where

import Text.ParserCombinators.Parsec
import Text.ParserCombinators.Parsec.Combinator

data Arg = Reg Char | Lit Int deriving Show
data Instr = Cpy Arg Arg
           | Inc Arg
           | Dec Arg
           | Jnz Arg Arg
           deriving Show

int = do
  sign <- (char '-' *> pure negate) <|> pure id
  sign . read <$> many1 digit

arg = space *> (Lit <$> int
                <|> Reg <$> anyChar)

bytecode name f = f <$> (string name *> arg)

instr :: CharParser () Instr
instr = bytecode "cpy" Cpy <*> arg
    <|> bytecode "inc" Inc
    <|> bytecode "dec" Dec
    <|> bytecode "jnz" Jnz <*> arg

parseInstr :: String -> Instr
parseInstr = either (error "no parse") id . runParser instr () "input"
