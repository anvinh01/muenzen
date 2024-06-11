<script lang="ts">
	import { onMount } from 'svelte';

	// SVG names
	let QuestionIcon: string = '';
	let HeadsIcon: string = '';
	let TailsIcon: string = '';

	// Fetch the SVGs from public/assets/ when the component is mounted
	onMount(async () => {
		// import the SVG for the Heads Coin
		const res = await fetch('public/assets/Kopf.svg');
		HeadsIcon = await res.text();

		// import the SVG for the Tails Coin
		const res2 = await fetch('public/assets/Zahl.svg');
		TailsIcon = await res2.text();

		// import the SVG for the Question Icon (null selection)
		const res3 = await fetch('public/assets/question-icon.svg');
		QuestionIcon = await res3.text();
	});

	// Set the selection_array to a prop and as an empty array per default
	export let selection_array: { id: string; value: string | null }[] = [];
</script>


<ul class="flex gap-4 center w-max-[60vw] flex-wrap mobile: mobile:gap-5 mobile:w-full mobile:justify-evenly">
	<!-- Going through the selection_array array and displaying the correct icon for each coin. -->
	{#each selection_array as coin}
		<!-- eslint-disable-next-line svelte/no-at-html-tags -->
		<div class="card w-[100px] h-[100px] mobile:w-auto mobile:h-auto group transition-all flip-card {coin.value ? 'active' : 'neutral'}">
			<div class="flip-card-inner mobile:hidden">
				<div class="icon w-full h-full flip-card-front">
					{@html QuestionIcon}
				</div>
				<div class="icon w-full h-full flip-card-back {coin.value}">
					{@html coin.value == null ? QuestionIcon :  coin.value === "heads" ? HeadsIcon : TailsIcon}
				</div>
			</div>
			<div class="flip-card-inner invisible mobile:visible text-black ">
				<div class="icon flip-card-front">
					<p>?</p>
				</div>
				<div class="icon flip-card-back prose font-black">
					<p>{coin.value == null ? "?" : coin.value === "heads" ? "K" : "Z"}</p>
				</div>
			</div>
		</div>
	{/each}
</ul>

<style>
	
.flip-card {
  background-color: transparent;
  perspective: 1000px;
}

.flip-card-inner {
  position: relative;
  width: 100%;
  height: 100%;
  text-align: center;
  transition: transform 0.6s;
  transform-style: preserve-3d;
}

.flip-card.active .flip-card-inner {
  transform: rotateY(180deg);
}

.flip-card-front, .flip-card-back {
  position: absolute;
  width: 100%;
  height: 100%;
  -webkit-backface-visibility: hidden;
  backface-visibility: hidden;
}


.flip-card-back {
  transform: rotateY(180deg);
}
</style>
