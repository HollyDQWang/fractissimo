source activate magenta

music_vae_generate \
--config=hierdec-trio_16bar \
--checkpoint_file=./hierdec-trio_16bar/hierdec-trio_16bar.ckpt \
--mode=interpolate \
--num_outputs=3 \
--input_midi_1=./generated/1.mid
--input_midi_2=./generated/2.mid
--output_dir=./interpolated