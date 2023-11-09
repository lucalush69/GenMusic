from pydub import AudioSegment, effects
import os
import contextlib, io
import matchering as mg
import random
from PIL import Image
from moviepy.editor import AudioFileClip, ImageClip
from cleanup import Clean
import CreateLayers
""""
This Script Creates Randomized Generative Music NFTs.
Reads Music Stems files, assigns them random weights, and then selects one from each category.
Merges the Audio files, mixes and masters them according to a reference track.
Then reads the visual stem files, selects the corresponding image, and composites a .Png
The subsequent png and audio file are combined into an .mp4 (the final NFT product)
"""


#Starts Here - Create the Folders
def CreateList():
    if not os.path.exists('stems/kicksnare_files'):
        os.mkdir('stems/kicksnare_files')
    kicksnare_files = os.listdir('stems/kicksnare_files')

    if not os.path.exists('stems/percussion_files'):
        os.mkdir('stems/percussion_files')
    percussion_files = os.listdir('stems/percussion_files')

    if not os.path.exists('stems/vocal_files'):
        os.mkdir('stems/vocal_files')
    vocals_files = os.listdir('stems/vocal_files')

    if not os.path.exists('stems/melodic_files'):
        os.mkdir('stems/melodic_files')
    melodic_files = os.listdir('stems/melodic_files')

    if not os.path.exists('stems/fx_files'):
        os.mkdir('stems/fx_files')
    fx_files = os.listdir('stems/fx_files')

    if not os.path.exists('stems/bass_files'):
        os.mkdir('stems/bass_files')
    bass_files = os.listdir('stems/bass_files')

    if not os.path.exists('stems/combined_files'):
        os.mkdir('stems/combined_files')
    combined_files = os.listdir('stems/combined_files')

    if not os.path.exists('stems/mastered_files'):
        os.mkdir('stems/mastered_files')
    mastered_files = os.listdir('stems/mastered_files')
    
    Files = [kicksnare_files, percussion_files, vocals_files, melodic_files, fx_files, bass_files]
    RarityCreator(Files)
    t = 0
    #HOW MANY TO MINT
    while t < 1:
        Selector(Files, kicksnare_files, percussion_files, vocals_files, melodic_files, fx_files, bass_files)
        t+=1

#Assigns randomzied rarity weights for each file but can be hardcoded if desired
def RarityCreator(Files):
    x=0
    for step in Files:
            print(step)
            length = len(step)
            print(length)
            randomlist = []
            for i in range(length):
                    n = random.randint(1,100)
                    randomlist.append(n)
                    print(randomlist)
            #weights = [50, 30, 14, 5, 1]
            RarityList[x] = randomlist
            x+=1 
    print(RarityList)
    print(RarityList[0])

#Checks to see if Combination already Exists, If not, 
def Selector(Files, kicksnare_files, percussion_files, vocals_files, melodic_files, fx_files, bass_files):
    count=0
    Choices = []
    storage = ""
    for step in Files:
            wlist = (RarityList[count])
            print(wlist)
            Pos = random.choices(step, wlist)[0]
            print(Pos)
            val = step.index(Pos)
            Choices.append(val)
            valstr = str(val)
            print(valstr)
            storage += valstr
            print(storage)
            count+=1
    if storage in DupCheck:
        print("Combination already existes, re-rolling")
        Selector(Files)
    else:
        print("Combination does not exist, Mintable")
        DupCheck.append(storage)
        total = storage
        print(DupCheck)
        print(Choices)
        kPos = int(Choices[0])
        pPos = int(Choices[1])
        vPos = int(Choices[2])
        mPos = int(Choices[3]) 
        fPos = int(Choices[4]) 
        bPos = int(Choices[5]) 

        ks = kicksnare_files[kPos]
        ps = percussion_files[pPos]
        vs = vocals_files[vPos]
        ms = melodic_files[mPos]
        fs = fx_files[fPos]
        bs = bass_files[bPos]
        
        kp = kicksnare_files.index(ks)
        pp = percussion_files.index(ps)
        vp = vocals_files.index(vs)
        mp = melodic_files.index(ms)
        fp = fx_files.index(fs)
        bp = bass_files.index(bs)
        name = (kp, pp, vp, mp, fp, bp)
        print(total, ks, ps, vs, ms, fs, bs)
        print(name)
        StemImport(total, ks, ps, vs, ms, fs, bs, name, Choices, storage)

#import 6 stems, normalize, mix, and export.
def StemImport(total, ks, ps, vs, ms, fs, bs, name, Choices, storage): 
    #import each stem 
    kicksnare = AudioSegment.from_file('stems\\kicksnare_files\\'+ks) 
    percussion = AudioSegment.from_file('stems\\percussion_files\\'+ps)
    vocals = AudioSegment.from_file('stems\\vocal_files\\'+vs)
    melodic = AudioSegment.from_file('stems\\melodic_files\\'+ms)
    fx = AudioSegment.from_file('stems\\fx_files\\'+fs)
    bass = AudioSegment.from_file('stems\\bass_files\\'+bs)

    #Normalize and Mix Each Stem 
    effects.normalize(kicksnare)
    kicksnareMixed = match_target_amplitude(kicksnare, -14.0)
    effects.normalize(percussion)
    percussionMixed = match_target_amplitude(percussion, -18.0)
    effects.normalize(vocals)
    vocalsMixed = match_target_amplitude(vocals, -19.0)
    effects.normalize(melodic)
    melodicMixed = match_target_amplitude(melodic, -24.0)
    effects.normalize(fx)
    fxMixed = match_target_amplitude(fx, -31.0)
    effects.normalize(bass)
    bassMixed = match_target_amplitude(bass, -21.0)

    #sequentially overlay each stem 
    combined = kicksnareMixed.overlay(percussionMixed)
    combined2 = combined.overlay(vocalsMixed)
    combined3 = combined2.overlay(melodicMixed)
    combined4 = combined3.overlay(fxMixed)
    combined5 = combined4.overlay(bassMixed)

    #lower the volume a bit
    effects.normalize(combined5)
    combinedNorm = match_target_amplitude(combined5, -20.0)

    #export the final product 
    newsong = combinedNorm.export('stems\\combined_files\\' +str(total) + str(".wav"), format='wav')
    mg.log(info_handler=print, warning_handler=print)

    #Use Matchering to Match the songs LUFS to a reference track
    mg.process(
        target= newsong,
        reference = "ukref.wav",
            results=[
                mg.pcm16('stems\\mastered_files\\mastered' + str(total) + str(name) + str(".wav"))
            ],
    )
    photoLay(Choices, storage)
    MintMerge(storage, total, name)            



#Create the Visual Aspect of the NFT    
def photoLay(Choices, storage):
        kPos = int(Choices[0])
        pPos = int(Choices[1])
        vPos = int(Choices[2])
        mPos = int(Choices[3]) 
        fPos = int(Choices[4]) 
        bPos = int(Choices[5]) 


        img1 = Image.open('VisualStems\\Background\\' +str("Background") +str(kPos) + str(".png"))
        img2 = Image.open('VisualStems\\Head\\' +str("Head") +str(pPos) +str(".png"))
        img5 = Image.open('VisualStems\\Eyes\\' +str("Eyes") +str(vPos) +str(".png"))
        img4 = Image.open('VisualStems\\Hat\\' +str("Hat") +str(mPos) +str(".png"))
        img3 = Image.open('VisualStems\\Nose\\' +str("Nose") +str(fPos) +str(".png"))
        img6 = Image.open('VisualStems\\Mouth\\' +str("Mouth") +str(bPos) +str(".png"))

        img1.paste(img2, (0,0), mask = img2)
        img1.paste(img3, (0,0), mask = img3)
        img1.paste(img4, (0,0), mask = img4)
        img1.paste(img5, (0,0), mask = img5)
        img1.paste(img6, (0,0), mask = img6)
        
        img1.show()
        img1.save('stems\\Visual_files\\' +str(storage) +str(".png"))

#Merge the Audio + Visual into an Mp4
def MintMerge(storage, total, name):
    # create the audio clip object
    audio_clip = AudioFileClip(r'stems\mastered_files\mastered' + str(total) + str(name) + str(".wav"))
    # create the image clip object
    image_clip = ImageClip(r'stems\Visual_files\\' +str(storage) +str(".png"))
    # use set_audio method from image clip to combine the audio with the image
    video_clip = image_clip.set_audio(audio_clip)
    # specify the duration of the new clip to be the duration of the audio clip
    video_clip.duration = audio_clip.duration
    # set the FPS to 1
    video_clip.fps = 1
    # write the resuling video clip
    video_clip.write_videofile('stems\\NFTs\\' +str(storage) + str(name) +str(".mp4"))
    
#changing volume of stems
def match_target_amplitude(sound, target_dBFS):
    change_in_dBFS = target_dBFS - sound.dBFS
    return sound.apply_gain(change_in_dBFS)

#Will Add headless mode functionality
#CreateLayers.Run()

DupCheck = []
RarityList = {}
CreateList()
visual_dir = 'stems/Visual_files'
combined_dir = 'stems/combined_files'
Clean(visual_dir)
Clean(combined_dir)




