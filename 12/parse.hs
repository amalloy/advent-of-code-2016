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

instr :: CharParser () Instr
instr = Cpy <$> (string "cpy" *> arg) <*> arg
    <|> Inc <$> (string "inc" *> arg)
    <|> Dec <$> (string "dec" *> arg)
    <|> Jnz <$> (string "jnz" *> arg) <*> arg

parseInstr :: String -> Instr
parseInstr = either undefined id . runParser instr () "input"

main = interact $ unlines . map (show . parseInstr) . lines
