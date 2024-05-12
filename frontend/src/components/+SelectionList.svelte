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
	export let selection_array: { id: number; value: string | null }[] = [];
</script>


<ul class="flex gap-4 justify-between">
	<!-- Going through the selection_array array and displaying the correct icon for each coin. -->
	{#each selection_array as coin (coin.id)}
		{#if coin.value == null}
			<!-- eslint-disable-next-line svelte/no-at-html-tags -->
			<div class="icon w-[100px] h-[100px] p-3 unknown">{@html QuestionIcon}</div>
		{:else if coin.value === 'Kopf'}
			<!-- eslint-disable-next-line svelte/no-at-html-tags -->
			<div class="icon w-[100px] h-[100px] Kopf">{@html HeadsIcon}</div>
		{:else if coin.value === 'Zahl'}
			<!-- eslint-disable-next-line svelte/no-at-html-tags -->
			<div class="icon w-[100px] h-[100px] Zahl">{@html TailsIcon}</div>
		{:else}
			<p>Invalid Input</p>
		{/if}
	{/each}
</ul>
