// Instantiate the model by loading the desired checkpoint.
const model = new mm.MusicVAE(
  'https://storage.googleapis.com/magentadata/js/checkpoints/music_vae/trio_4bar');
model.initialize().then(() => {
  document.getElementById('loading').style.display = 'none';
  [...document.getElementsByTagName('button')].forEach(b => b.style = '');
});

// Create a player.
const player = new mm.Player();

// Create a global trio for downloading.
let trio;

function play() {
  player.resumeContext(); // enable audio
  model.sample(1)
    .then((samples) => player.start(samples[0], 80));
}

function generate() {
  mm.Player.tone.context.resume();  // enable audio
  model.sample(1).then((samples) => {
    trio = samples[0];  // store trio for download
    player.start(trio);
  });
}

function download() {
  if (!trio) {
    alert('You must generate a trio before you can download it!');
  } else {
    saveAs(new File([mm.sequenceProtoToMidi(trio)], 'trio.mid'));
  }
}

function interpolate() {

}