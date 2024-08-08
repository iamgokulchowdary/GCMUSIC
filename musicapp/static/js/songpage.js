$(document).ready(function() {
    const $audio = $('#audio');
    const $playButton = $('#play');
    const $pauseButton = $('#pause').hide();
    const $nextButton = $('#next');
    const $prevButton = $('#previous');
    const $repeatButton = $('#repeat');
    const $likeButton = $('#like');
    const $addToPlaylistButton = $('#addtoplaylist');
    const $songLengthSlider = $('#songlength');
    const $volumeSlider = $('#volumeslider');

    // let currentSongIndex = 0;
    // const songs = [
    //     { name: 'Song 1', artist: 'Artist 1', file: 'songs/song1.mp3' },
    //     { name: 'Song 2', artist: 'Artist 2', file: 'songs/song2.mp3' },
    //     { name: 'Song 3', artist: 'Artist 3', file: 'songs/song3.mp3' }
    // ];

    // function loadSong(index) {
    //     const song = songs[index];
    //     $audio.attr('src', song.file);
    //     $('.songdetails h4').text(song.name);
    //     $('.songdetails p').text(song.artist);
    //     $audio[0].load();
    // }

    // loadSong(currentSongIndex);

    $volumeSlider.val(100);
    
    $playButton.on('click', function() {
        $audio[0].play();
        $playButton.hide();
        $pauseButton.show();
    });

    $pauseButton.on('click', function() {
        $audio[0].pause();
        $playButton.show();
        $pauseButton.hide();
    });

    $audio.on('timeupdate', function() {
        const percentage = ($audio[0].currentTime / $audio[0].duration) * 100;
        $songLengthSlider.val(percentage);
    });

    $songLengthSlider.on('input', function() {
        const percentage = $(this).val();
        $audio[0].currentTime = ($audio[0].duration / 100) * percentage;
    });

    $volumeSlider.on('input', function() {
        $audio[0].volume = $(this).val() / 100;
    });

    $repeatButton.on('click', function() {
        $audio[0].loop = !$audio[0].loop;
        $(this).find('i').toggleClass('repeaton');
    });

    $likeButton.on('click', function() {
        $(this).find('i').toggleClass('liked');
    });

    // $addToPlaylistButton.on('click', function() {
    //     alert('Added to playlist');
    // });

    // $nextButton.on('click', function() {
    //     currentSongIndex = (currentSongIndex + 1) % songs.length;
    //     loadSong(currentSongIndex);
    //     if ($playButton.is(':hidden')) {
    //         $audio[0].play();
    //     }
    // });

    // $prevButton.on('click', function() {
    //     currentSongIndex = (currentSongIndex - 1 + songs.length) % songs.length;
    //     loadSong(currentSongIndex);
    //     if ($playButton.is(':hidden')) {
    //         $audio[0].play();
    //     }
    // });
});