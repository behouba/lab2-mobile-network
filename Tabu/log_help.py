if __name__ == "__main__":
    with open("debug_9.log") as fr, open("debug_9_2.log", 'w') as fw:
        for line in fr:
            if "-> comm" in line:
                fw.write(line)
