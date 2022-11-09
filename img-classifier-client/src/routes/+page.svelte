<script lang="ts">
	import { onMount } from 'svelte';

	const block_count = 28;
	// pixel size
	const px = 10;

	let image_values = new Int8Array(784).fill(0);

	let canvas: HTMLCanvasElement;
	let ctx: CanvasRenderingContext2D | null;

	let draw_mode = false;
	let mouse_pos = {
		x: 0,
		y: 0
	};

	function make_background() {
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
	}

	function draw_pixel({ x, y }: { x: number; y: number }) {
		const index = Math.floor(x / px) + block_count * Math.floor(y / px);
		if (ctx) {
			ctx.strokeStyle = '#aaa';
			ctx.fillStyle = '#000';
			ctx.fillRect(x - (x % px), y - (y % px), px, px);
			ctx.strokeRect(x - (x % px), y - (y % px), px, px);
			image_values[index] = 255;
		}
	}

	function draw(event: MouseEvent & { currentTarget: EventTarget & HTMLCanvasElement }) {
		const canvas_rect = canvas.getBoundingClientRect();
		mouse_pos = {
			x: Math.floor(event.clientX - canvas_rect.left),
			y: Math.floor(event.clientY - canvas_rect.top)
		};
		// draw_pixel({ x: mouse_pos.x, y: mouse_pos.y - px });
		draw_pixel({ x: mouse_pos.x, y: mouse_pos.y + px });
		// draw_pixel({ x: mouse_pos.x - px, y: mouse_pos.y });
		draw_pixel({ x: mouse_pos.x + px, y: mouse_pos.y });

		draw_pixel({ x: mouse_pos.x, y: mouse_pos.y });
	}

	onMount(() => {
		make_background();
	});
</script>

<h1>Draw an Digit</h1>
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
		if (draw_mode) draw(event);
	}}
	on:click={(event) => {
		draw(event);
	}}
	width={block_count * px}
	height={block_count * px}
/>

<style>
	.canvas {
		background-color: gray;
		border: 1px solid black;
	}
</style>
