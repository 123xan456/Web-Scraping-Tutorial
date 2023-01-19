from GenerateICUtils import generate_IC

checkpoint = open("ckpt.txt", "r+")
ckpt = checkpoint.read()
generate_IC(ckpt)
