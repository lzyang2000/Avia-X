
quiet = 'Quiet Theme'
engaged = 'Engaged Theme'
cozy = 'Cozy'
reading = 'Concentrated'

image = 'Image'
light = 'Light'
music = 'Music'
seat_angle = 'Seat Angle'
reading_light = 'Reading Light'
entertainment_recommendation = 'Entertainment Recommendation'

# All paths could be handled more elegantly. More on this later
preset_global_themes = {
    quiet: { image: ['./quiet_theme/photos/1.png', './quite_theme/photos/2.png'], light: 70, music: './quite_theme/music_playlist' },
    engaged: { image: ['./engaged_theme/photos/1.png', './engaged_theme/photos/2.png'], light: 70, music: './engaged_theme/music_playlist' },
}

preset_personal_themes = {
    cozy: { seat_angle: 25, entertainment_recommendation: [], reading_light: 0 },
    reading: { seat_angle: 80, entertainment_recommendation: [], reading_light: 40 }
}
