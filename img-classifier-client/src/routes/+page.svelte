<script lang="ts">
	import { onMount } from 'svelte';

	const block_count = 28;
	// pixel size
	const px = 10;

	let ai_guess: number = -1;

	let image_values = new Uint8Array(784).fill(0);

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
			ctx.strokeStyle = '#ffffff';
			ctx.fillStyle = '#000000';
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
			ctx.fillStyle = '#fff';
			ctx.strokeStyle = '#000';
			ctx.fillRect(x - (x % px), y - (y % px), px, px);
			ctx.strokeRect(x - (x % px), y - (y % px), px, px);
			image_values[index] = 255;
		}
	}

	function draw(e: MouseEvent & { currentTarget: EventTarget & HTMLCanvasElement }) {
		const canvas_rect = canvas.getBoundingClientRect();
		mouse_pos = {
			x: Math.floor(e.clientX - canvas_rect.left),
			y: Math.floor(e.clientY - canvas_rect.top)
		};
		// draw_pixel({ x: mouse_pos.x, y: mouse_pos.y - px });
		draw_pixel({ x: mouse_pos.x, y: mouse_pos.y + px });
		// draw_pixel({ x: mouse_pos.x - px, y: mouse_pos.y });
		draw_pixel({ x: mouse_pos.x + px, y: mouse_pos.y });

		draw_pixel({ x: mouse_pos.x, y: mouse_pos.y });
	}

  function resetImage(e: MouseEvent&{ currentTarget: EventTarget&HTMLButtonElement; }) {
    e.preventDefault();
    image_values = image_values.fill(0);
    make_background();
    ai_guess = -1;
  }

	function sendToAI(e: MouseEvent & { currentTarget: EventTarget & HTMLButtonElement }) {
		e.preventDefault();

		fetch('http://localhost:4000/ai', {
			headers: {
				'Content-Type': 'application/octet-stream'
			},
			method: 'post',
			body: image_values
		})
			.then((data) => data.blob())
      .then(data => data.arrayBuffer())
      .then(data => new Uint8Array(data))
      .then(data => ai_guess = data[1])
			.catch((err) => console.error(err));
	}

	onMount(() => {
		make_background();
	});
</script>

<h1>Draw an Digit</h1>
<p>mouse position {mouse_pos.x} {mouse_pos.y}</p>

<div class="container">
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
	<div>
		<button on:click={e => resetImage(e)}>reset</button>
		<button on:click={(e) => sendToAI(e)}>check with AI</button>
	</div>

	<div>
		<h2>What the AI thinks</h2>
		{#if ai_guess > -1}
			<h2>{ai_guess}</h2>
		{/if}
	</div>
</div>

<style>
  .container {
    display: grid;
    grid-template-columns: auto auto auto;
  }
	.canvas {
		background-color: gray;
		border: 1px solid black;
	}
</style>
