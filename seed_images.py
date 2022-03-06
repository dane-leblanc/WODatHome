from models import db, ExerciseImage
from app import app
import fetch

ExerciseImage.__table__.drop(db.engine)
ExerciseImage.__table__.create(db.engine)

images = []

def add(id, url):
    new_image = ExerciseImage(
        exercise_id = id,
        image_url = url,
    )
    images.append(new_image)

# two handed kettlebell
add(345, "https://media.giphy.com/media/KFbeRdU6rtlsTyJ7va/giphy-downsized-large.gif")

# arnold press
add(227, "https://media.giphy.com/media/jtVqKOyQqglvJ9itlo/giphy.gif")

# back squat
add(637, "https://media.giphy.com/media/nU5Tnm67uh0HBZozWA/giphy.gif")

# barbell ab rollout
add(343, "https://i.makeagif.com/media/10-08-2015/0JkO-3.gif")

# barbell hack squat
add(407, "https://www.strengthlog.com/wp-content/uploads/2021/11/Barbell-Hack-Squat.gif")

# barbell lunges
add(405, "https://i0.wp.com/www.strengthlog.com/wp-content/uploads/2020/03/Barbell-Lunge.gif?fit=600%2C600&ssl=1")

# barball triceps extension
add(344, "https://i0.wp.com/www.strengthlog.com/wp-content/uploads/2020/03/Barbell-Standing-Triceps-Extension.gif?fit=600%2C600&ssl=1")

# bear walk
add(307, "https://i.pinimg.com/originals/0e/c0/24/0ec0249c8586715e2ccd247e27054fd9.gif")

# bench press
add(192, "https://thumbs.gfycat.com/ClearHalfHoatzin-size_restricted.gif")

# bench press (dumbbells)
add(97, "https://images.squarespace-cdn.com/content/v1/54f9e84de4b0d13f30bba4cb/1526590877144-BYR9X8ZX5FROTGOZ2VHL/DSC_6330.mov.gif")

# bench press narrow grip
add(88, "https://9to5strength.com/wp-content/uploads/2016/09/Close-Grip-Bench-Press.gif")

# bent high pulls
add(268, "https://thumbs.gfycat.com/WigglyPoliticalAuk-size_restricted.gif")

# bent over barbell row
add(412, "https://hips.hearstapps.com/hmg-prod.s3.amazonaws.com/images/workouts/2017/04/barbellrow-1491916911.gif")

# bent over dumbbell row
add(362, "https://www.nerdfitness.com/wp-content/uploads/2019/10/steve-dumbbell-row.gif")

# bent over lateral raises
add(421, "https://thumbs.gfycat.com/MediumWelllitDutchsmoushond-size_restricted.gif")

# bent over laterals
add(919, "https://thumbs.gfycat.com/VigilantEntireFrilledlizard-size_restricted.gif")

# bent over rowing
add(109, "https://www.nerdfitness.com/wp-content/uploads/2019/10/steve-dumbbell-row.gif")

# bent over rowing reverse
add(110, "https://media3.giphy.com/media/UUn6oTupFoo0T9g6jS/giphy.gif")

# biceps curl barbell
add(74, "https://i0.wp.com/www.strengthlog.com/wp-content/uploads/2020/12/Barbell-biceps-curl.gif?fit=600%2C600&ssl=1")

# biceps curl dumbbell
add(81, "https://thumbs.gfycat.com/FelineSaltyBat-size_restricted.gif")

# biceps curl sz-bar
add(80, "https://thumbs.gfycat.com/MeanTediousIriomotecat-max-1mb.gif")

# bulgarian split squat
add(914, "https://media4.giphy.com/media/g0Kz180GdPYCsKqMyf/giphy.gif")

# calf raises
add(776, "https://flabfix.com/wp-content/uploads/2019/06/Calf-Raises.gif")

# close grip bench press
add(217, "https://bodybuilding-wizard.com/wp-content/uploads/2014/04/close-grip-barbell-bech-press-animation-2.gif")

# crunches
add(91, "https://flabfix.com/wp-content/uploads/2019/05/Crunches.gif")

# chin up
add(803, "https://i0.wp.com/post.healthline.com/wp-content/uploads/2021/05/400x400_Chinup.gif?h=840")

# chin-ups
add(181, "https://i0.wp.com/post.healthline.com/wp-content/uploads/2021/05/400x400_Chinup.gif?h=840")

# decline bench press barbell
add(100, "https://thumbs.gfycat.com/DeepHeavyHuemul-max-1mb.gif")

# decline bench press dumbbell
add(101, "https://thumbs.gfycat.com/ElectricGlossyHuemul-size_restricted.gif")

# decline pushups
add(260, "https://flabfix.com/wp-content/uploads/2019/05/Decline-Elevated-Push-Ups.gif")

# deficit deadlift
add(381, "https://www.strengthlog.com/wp-content/uploads/2020/02/Defifict-deadlift.gif")

# diagonal shoulder press
add(329, "https://thumbs.gfycat.com/ExcitableOblongFluke-max-1mb.gif")

# dips
add(781, "https://j.gifs.com/Jy81qK.gif")

# dips between two benches
add(83, "https://media3.giphy.com/media/26xBCzMfXwx9WxbS8/giphy.gif")

# dumbbell concentration curl
add(275, "https://i0.wp.com/www.strengthlog.com/wp-content/uploads/2020/03/Concentration-curl.gif?fit=600%2C600&ssl=1")

# dumbbell goblet squat
add(300, "https://media1.giphy.com/media/3oKIPvcdnW1xs9m5IA/giphy.gif")

# dumbbell incline curl
add(298, "https://i0.wp.com/www.strengthlog.com/wp-content/uploads/2020/10/Incline-Dumbbell-Curl.gif?fit=600%2C600&ssl=1")

# dumbbell lunges standing
add(112, "https://i0.wp.com/www.strengthlog.com/wp-content/uploads/2020/03/Dumbbell-Lunge.gif?fit=600%2C600&ssl=1")

# dumbbell lunges walking
add(113, "https://media1.giphy.com/media/xT8qBrjcngCsejZ0mA/giphy.gif")

# dumbbell triceps extension
add(274, "https://media0.giphy.com/media/qakKR41BeNAi3eJc8z/200w.gif?cid=82a1493b36j87lumzhbxv989z8f828l4688zkytf3zpcvsgr&rid=200w.gif&ct=g")

# fly with dumbbells
add(145, "https://i0.wp.com/www.strengthlog.com/wp-content/uploads/2020/03/Dumbbell-Chest-Fly.gif?fit=600%2C600&ssl=1")

# fly with dumbbells, decline
add(146, "https://j.gifs.com/ElDANY.gif")

# forward lunge
add(874, "https://media4.giphy.com/media/SwgkfECuO4XylhLNuN/giphy.gif")

# french press/skullcrusher dumbbells
add(85, "https://i.makeagif.com/media/2-15-2014/vXbl05.gif")

# french press/skullcrusher sz-bar
add(84, "https://thumbs.gfycat.com/GiganticKlutzyAfricangroundhornbill-max-1mb.gif")

# front raises
add(233, "https://i0.wp.com/www.strengthlog.com/wp-content/uploads/2020/03/Dumbbell-Front-Raise.gif?fit=600%2C600&ssl=1")

# front squats
add(191, "https://i0.wp.com/www.strengthlog.com/wp-content/uploads/2021/09/Front-squat.gif?fit=600%2C595&ssl=1")

# rear delt raises
add(237, "https://thumbs.gfycat.com/AfraidLawfulCob-max-1mb.gif")

# full sit outs
add(326, "https://cdn.mos.cms.futurecdn.net/zX9F7uj6H7TMGeDn3oNc8U-970-80.jpg.webp")

# hammer curls 
add(86, "https://www.strengthlog.com/wp-content/uploads/2020/02/Hammer-curl.gif")

# handstand pushup
add(807, "https://www.verywellfit.com/thmb/9_suoh9PO1Zc6KHXqX0fAT45Rxg=/1000x1000/smart/filters:no_upscale()/49-Handstand-Push-Up-GIF-resize-acd4704473024e71a2f1e3057feae6dd.gif")

# hip raise, lying
add(376, "https://i.pinimg.com/originals/2d/84/be/2d84be3e561ecaaa7aa1334e63039ad6.gif")

# hip thrust
add(854, "https://c.tenor.com/pM6vr8YZeuwAAAAC/hip-thrust-workout.gif")

# hollow hold
add(383, "https://images.squarespace-cdn.com/content/v1/5895fa91440243be53fb3d52/1558484731430-TPFK32DFS9STKWM85E7M/hollow+rock+no+notations.gif")

# incline bench press
add(163, "https://i0.wp.com/www.strengthlog.com/wp-content/uploads/2020/03/Incline-Bench-Press.gif?fit=600%2C600&ssl=1")

# incline dumbbell fly
add(206, "https://i.makeagif.com/media/9-28-2015/F8Ku-t.gif")

# incline dumbbell press
add(210, "https://www.strengthlog.com/wp-content/uploads/2020/03/Dumbbell-Incline-Press.gif")

# incline dumbbell row
add(340, "https://dsgmedia.blob.core.windows.net/pub/2019/07/Row-Facing-Bench.gif")

# isometric wipers
add(338, "https://thumbs.gfycat.com/AdvancedUnevenIndianelephant-size_restricted.gif")

# renegade row
add(670, "https://media4.giphy.com/media/1n6exUWUnxvyzkYAaG/200.gif")

# lateral raises
add(148, "https://i0.wp.com/www.strengthlog.com/wp-content/uploads/2020/12/Dumbbell-Lateral-Raise.gif?resize=600%2C600&ssl=1")

# lateral to front raises
add(306, "https://media1.popsugar-assets.com/files/thumbor/w64sHPKenbV9NwQGCy2b3MKalnI/fit-in/1024x1024/filters:format_auto-!!-:strip_icc-!!-/2020/08/17/758/n/1922729/9cbcde2281ff4a10_IMB_gX3l9q/i/Side-to-Front-Raise.GIF")

# let raises, lying
add(125, "https://thumbs.gfycat.com/CraftyOldFruitfly-max-1mb.gif")

# reverse bar curl
add(208, "https://9to5strength.com/wp-content/uploads/2016/07/1air70.gif")

# low box squat - wide stance
add(389, "https://images.squarespace-cdn.com/content/v1/5dd5c242b5660a572b0552b7/1579145122050-2OWQUYYT4RRZZ2AJT4NN/BoxSquat_Demo_03.gif")

# lying rotator cuff exercise
add(312, "https://thumbs.gfycat.com/EllipticalDeadChick-max-1mb.gif")

# military press
add(256, "https://thumbs.gfycat.com/ConsciousFabulousLadybug-size_restricted.gif")

# military press
add(229, "https://thumbs.gfycat.com/ConsciousFabulousLadybug-size_restricted.gif")

# muscle up
add(626, "https://c.tenor.com/dgCyChkdEY4AAAAC/muscle-up.gif")

# pause bench
add(270, "https://thumbs.gfycat.com/OrdinarySpryChrysalis-max-1mb.gif")

# pendelay rows
add(202, "https://i0.wp.com/www.strengthlog.com/wp-content/uploads/2020/10/pendlay-row.gif?fit=600%2C600&ssl=1")

# pike push up
add(361, "https://hips.hearstapps.com/hmg-prod.s3.amazonaws.com/images/workouts/2016/03/pikepushup-1456956895.gif")

# plank
add(238, "https://imagesvc.meredithcorp.io/v3/mm/image?url=https%3A%2F%2Fstatic.onecms.io%2Fwp-content%2Fuploads%2Fsites%2F35%2F2020%2F02%2Flow-plank-hold.jpg")

db.session.add_all(images)
db.session.commit()

# fetch.fill_images()