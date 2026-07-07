# Lesson 06 — Raspberry Pi 5: Linux & Remote Access

> Meet a computer the size of a deck of cards: the Linux desktop, the terminal, and (optionally) how to control your Pi from another machine.

**Platform:** Raspberry Pi 5
**Estimated time:** ~120 min hands-on
**Prerequisites:** [Lesson 5](lesson-05-arduino-project.md) — none of the Arduino skills are needed today, but the contrast matters

## The big idea

The Arduino is a **microcontroller**: it runs one sketch, forever, the instant power arrives. The Raspberry Pi 5 is a **full computer**: it boots an operating system (Linux), runs many programs at once, has files, users, a desktop, and a network. This changes what we can build — and how we work.

| | Arduino | Raspberry Pi 5 |
|---|---|---|
| Runs | One sketch | A whole OS (Linux) + your programs |
| Code | C++, compiled on the Mac, uploaded | Python, written & run **on the Pi itself** |
| Storage | None (just the sketch) | microSD card — real files |
| Network | No | Yes — Wi-Fi, browser, remote access |
| Turn off by | Pulling the plug | **Shutting down properly** |

## Learning objectives

- Boot the Pi, tour the desktop, and shut it down *properly*.
- Navigate and manage files from the **terminal**: `pwd`, `ls`, `cd`, `mkdir`, `cp`, `mv`, `rm`.
- Install software with `apt` and clone the course repo with `git`.
- Describe the three remote-access options (SSH, VNC, Raspberry Pi Connect) and when each is worth using — **all optional**.

## Today's plan (~120 min)

| Time | Part | What you're doing |
|---|---|---|
| ~20 min | A | Boot, desktop tour, settings, proper shutdown |
| ~40 min | B | **Core skill:** terminal essentials + scavenger hunt |
| ~25 min | C | Install software; clone the course repo onto your Pi |
| ~25 min | D | Remote access sampler (optional skills) |
| ~10 min | — | Check-out + shutdown |

## What you'll need

| Item | Qty | Notes |
|---|---|---|
| Raspberry Pi 5 (with imaged microSD) | 1 | Cards are pre-imaged for the class |
| Screen + HDMI cable, keyboard, mouse | 1 set | Provided at your bench |
| Pi power supply (USB-C, 27 W) | 1 | Use the official one — not a phone charger |

---

## Part A — Boot, tour, shutdown (~20 min)

1. Connect HDMI, keyboard, mouse **first**, power **last** — the Pi boots the moment power arrives.
2. Watch it boot into the Raspberry Pi OS desktop. Explore: the menu (top-left), the file manager, the browser, **Thonny** (menu → Programming — that's Lesson 7's home).
3. Open the terminal (the black icon in the taskbar). Leave it open — it's the star of Part B.

!!! warning "Never just pull the plug"
    The Pi writes to its microSD card constantly. Cutting power mid-write can corrupt the card — that's a re-image and lost work. Always **menu → Shutdown**, wait for the green LED to stop flashing, *then* unplug.

---

## Part B — Core skill: the terminal (~40 min)

The desktop is fine, but the terminal is *faster*, works over remote connections, and is how the Whisplay driver gets installed in Lesson 10. Work through these — type them, don't just read them:

```bash
pwd             # where am I? (print working directory)
ls              # what's here?
ls -l           # ...with details (size, date, permissions)
cd Documents    # move into a folder
cd ..           # go up one level
cd ~            # jump home from anywhere
mkdir apc       # make a folder
cp file.txt backup.txt    # copy
mv old.txt new.txt        # move / rename
rm unwanted.txt           # delete (NO undo — no trash bin here!)
```

!!! tip "The two keys that make you fast"
    **Tab** completes names (type `cd Doc` + Tab). **↑** recalls previous commands. Terminal veterans are just people who press Tab a lot.

### ✅ Checkpoint B — scavenger hunt

From your home folder, using **only the terminal**:

1. Make a folder `apc/lesson-06`.
2. Inside it, create a file with your name in it: `echo "built by YOURNAME" > about.txt`
3. Prove it: `cat apc/lesson-06/about.txt`
4. Rename it to `signature.txt`, then show a teacher `ls -l` of the folder.

---

## Part C — Install software & clone the repo (~25 min)

Linux installs software from the command line with `apt` (like a command-line app store):

```bash
sudo apt update          # refresh the package list
sudo apt install htop    # a live system monitor — try it! (q to quit)
```

`sudo` means "do this as administrator" — the Pi will ask for your password.

Now put the course code on your Pi (this is Lesson 1's git skill, for real this time):

```bash
cd ~/apc
git clone https://github.com/dominicmooney007/APC_2026-27.git
ls APC_2026-27/code      # there's every lesson's code
```

### ✅ Checkpoint C

Run `python3 APC_2026-27/code/lesson-01/clone_check.py` — the Lesson 1 checkpoint file, now running *on the Pi*.

---

## Part D — Remote access sampler (~25 min, optional skills)

Your bench always has a screen and keyboard — you never *need* remote access. But three ways exist to drive the Pi from your Mac, and each is a real-world skill:

| Method | You get | Best for |
|---|---|---|
| **SSH** | The Pi's *terminal* in a window on your Mac | Quick commands, feels professional |
| **VNC** | The Pi's whole *desktop* in a window | When you want the GUI remotely |
| **Raspberry Pi Connect** | Desktop or shell *via the browser* | Zero setup on the Mac, works anywhere |

Try SSH now (Pi and Mac on the same network):

```bash
# on the Pi, find its address:
hostname -I

# on the Mac's Terminal (use your Pi's username and address):
ssh pi@192.168.1.42
```

Type `exit` to leave. VNC and Pi Connect demos at the front bench for anyone curious.

!!! note "Optional means optional"
    Everything in this course works with the screen and keyboard in front of you. Use remote access if you like it; skip it if you don't.

---

## Check your work

You're done today when: you've completed both checkpoints, tried SSH once, and **shut your Pi down properly**.

## Extension / challenge

1. **Command detective** — find out what `df -h`, `uname -a`, and `vcgencmd measure_temp` tell you about your Pi.
2. **Alias magic** — add `alias apc='cd ~/apc/APC_2026-27'` to your `~/.bashrc` and reload with `source ~/.bashrc`. Now typing `apc` teleports you to the course repo.

## Code

- [`code/lesson-06/terminal_scavenger_hunt.md`](https://github.com/dominicmooney007/APC_2026-27/blob/main/code/lesson-06/terminal_scavenger_hunt.md) — the Checkpoint B tasks + a command cheat-sheet to keep.

**Next up:** [Lesson 7 — Raspberry Pi: Python, Thonny & GPIO](lesson-07-pi-gpio.md)
