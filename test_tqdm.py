from tqdm import trange
import time

bar = trange(int(1711122869 - time.time()))

for i in bar:
    time.sleep(0.5)
    bar.set_description(f"已等待 {i/2}s")
