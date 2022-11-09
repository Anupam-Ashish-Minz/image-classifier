<script lang="ts">
	let draw_mode = false;
	let mouse_pos = {
		x: 0,
		y: 0
	};
</script>

<h1>Draw an image</h1>
<p>mouse position {mouse_pos.x} {mouse_pos.y}</p>

<canvas
	class="canvas"
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
		width: 560px;
		height: 560px;
	}
</style>
