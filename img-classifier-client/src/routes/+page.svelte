<script lang="ts">
	import { onMount } from 'svelte';

	const block_count = 28;
  // pixel size
	const px = 20;

	let canvas: HTMLCanvasElement;
	let ctx;

	let draw_mode = false;
	let mouse_pos = {
		x: 0,
		y: 0
	};

	onMount(() => {
		ctx = canvas.getContext('2d');
		if (ctx) {
			ctx.fillStyle = '#ffffff';
			ctx.strokeStyle = '#000000';
			for (let i = 0; i < block_count; i++) {
				for (let j = 0; j < block_count; j++) {
					ctx.strokeRect(i * px, j * px, px, px);
					ctx.fillRect(i * px, j * px, px, px);
				}
			}
		}
	});
</script>

<h1>Draw an image</h1>
<p>mouse position {mouse_pos.x} {mouse_pos.y}</p>

<canvas
	class="canvas"
	bind:this={canvas}
	on:mouseup={() => {
		draw_mode = false;
	}}
	on:mousedown={() => {
		draw_mode = true;
	}}
	on:mousemove={(event) => {
		if (draw_mode)
			mouse_pos = {
				x: event.clientX,
				y: event.clientY
			};
	}}
	width="560px"
	height="560px"
/>

<style>
	.canvas {
		background-color: gray;
		border: 1px solid black;
	}
</style>
