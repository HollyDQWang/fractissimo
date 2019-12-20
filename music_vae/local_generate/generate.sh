
source activate magenta

music_vae_generate \
--config=hierdec-trio_16bar \
--checkpoint_file=hierdec-trio_16bar.tar \
--mode=sample --num_outputs=2 \
--output_dir=./generated