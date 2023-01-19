from Utils.GenerateICUtils import generate_IC

checkpoint = open("Res/ckpt.txt", "r+")
ckpt = checkpoint.read()
generate_IC(ckpt)
