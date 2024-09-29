#!/usr/bin/env python3

WITH_EYETRACKER = True

# Load Chamois:
exec(open("chamois.py").read())

if WITH_EYETRACKER:
  exec(open("TPx.py").read())

# Change theme:
theme('Black')

font = "Courier"
fontsize = 22
wordspacing = 10

#
# Load stimuli:
#

practice_sentences = load_stimuli("practice_sentences.tsv")
target_sentences   = load_stimuli("target_sentences.tsv")
filler_sentences   = load_stimuli("filler_sentences.tsv")

# Mix and shuffle:
stimuli = next_latin_square_list(target_sentences)
stimuli += filler_sentences
random.shuffle(stimuli)

#
# Structure of the experiment:
#

if WITH_EYETRACKER:
  tpx = TPx()

# An experiment consists of a series of pages:
pages = []

# Welcome screen:
pages.append(ConsentForm("""
Vielen Dank, dass Sie an dieser Studie teilnehmen!

Im Rahmen der Studie werden Sie Sätze lesen und Fragen zu deren Inhalt beantworten.  Ihre
Augenbewegungen werden dabei mit einer Kamera aufgezeichnet.  Es sind keine
Risiken oder Nebenwirkungen bekannt.

Der Erfolg dieser Studie hängt von Ihrer Mitarbeit ab.  Wir bitten Sie daher,
während der gesamten Dauer konzentriert zu bleiben.

Alle aufgezeichneten Daten werden anonymisiert gespeichert."""))

# Calibration:
if WITH_EYETRACKER:
  pages.append(
    CenteredInstructions("Bevor wir beginnen, müssen wir den Eye-Tracker kalibrieren."))
  pages.append(TPxCalibration(tpx))

# Explain practice sentences:
pages.append(
  CenteredInstructions("""
  Zuerst werden wir mit einigen Sätze üben.

  Der Ablauf ist folgender:

  1. Schauen Sie auf den blinkenden Kreis, der links erscheint.
  2. Lesen Sie den Satz dann in Ihrem eigenen Tempo, bis Sie ihn verstehen.
  3. Wenn Sie fertig sind, schauen Sie auf den Kreis in der unteren rechten Ecke
     um fortzufahren.
  4. Es erscheint eine Ja/Nein-Frage.  Um zu antworten, drücken Sie
     die Taste "f" für "Nein" und die Taste "j" für "Ja".

  Legen Sie nun Ihre Zeigefinger auf die Tasten 'f' und 'j', damit Sie
  nicht danach suchen müssen, wenn die Frage erscheint."""))


# practice_sentences = [[101, "practice", "Tina praised the gardeners of the millionaire who have recently installed a solar powered sprinkler.", "Question"]]
# practice_sentences = []

for i,c,s,q in practice_sentences:
  if WITH_EYETRACKER:
    pages.append(TPxReadingTrial(i,c,s,tpx))
  else:
    pages.append(ReadingTrial(i,c,s))
  pages.append(YesNoQuestionTrial(i,c,q))
  pages.append(TPxNext(tpx))
pages.pop()

# Explain experimental trials:
pages.append(
  CenteredInstructions("""
  Super! Nun zum Hauptteil, der etwas länger dauern wird.

  Der Ablauf ist derselbe, 
  nur dass die Fragen erst nach einigen Sätzen angezeigt werden.

  Sie können jederzeit eine Pause machen, aber am besten 
  nach Beendigung eines Satz oder einer Frage.

  Legen Sie bitte Finger auf die ’f’ und ’j’ Tasten."""))

for i,c,s,q in stimuli:
  if WITH_EYETRACKER:
    pages.append(TPxReadingTrial(i,c,s,tpx))
  else:
    pages.append(ReadingTrial(i,c,s))
  if random.choice([True, False]):
    pages.append(YesNoQuestionTrial(i,c,q))
  pages.append(TPxNext(tpx))
pages.pop()

# Thank you screen:
pages.append(
  CenteredInstructions("Geschafft!  Vielen herzlichen Dank für Ihre Teilnahme."))

# Run experiment:
run_experiment(pages)

