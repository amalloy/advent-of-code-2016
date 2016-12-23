data Arg = Lit Int | Reg String deriving Show
data Instruction = Cpy Arg Arg
                 | Inc Arg
                 | Dec Arg
                 | Jnz Arg Arg
                 | Tgl Arg
                 | Add Arg Arg
                 deriving Show

optimizeAdditionLoops :: [Instruction] -> [Instruction]
optimizeAdditionLoops [] = []
optimizeAdditionLoops (a:rest@(b:Jnz (Reg r) (Lit (-2)):xs)) =
  case (a, b) of
    (Inc ra@(Reg a'), Dec rb@(Reg b')) | b' == r -> go ra rb
    (Dec rb@(Reg b'), Inc ra@(Reg a')) | b' == r -> go ra rb
    _ -> a : optimizeAdditionLoops rest
  where go a b = Add a b :
                 (Jnz (Lit 0) (Lit 0)) :
                 (Jnz (Lit 0) (Lit 0)) :
                 optimizeAdditionLoops xs
optimizeAdditionLoops (x:xs) = x : optimizeAdditionLoops xs
