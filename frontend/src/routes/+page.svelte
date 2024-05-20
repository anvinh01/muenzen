<script lang="ts">
    import { onMount } from 'svelte';
    import SelectionList from '../components/+SelectionList.svelte'; // Adjusted import
    import { fade } from'svelte/transition';


    // SVG names
    let svgHero: string = '';
    let svgTask: string = '';
    let HeadsIcon: string = '';
    let TailsIcon: string = '';
    // Fetch the SVGs from public/assets/ when the component is mounted
    onMount(async () => {
        // import the SVG for the hero section
        const res = await fetch('public/assets/Coins-pana 1.svg');
        svgHero = await res.text();

        // import the SVG for the task section
        const res2 = await fetch('public/assets/Browser stats-pana 1.svg');
        svgTask = await res2.text();

        // import the SVG for the Heads Coin
        const res3 = await fetch('public/assets/heads-big.svg');
        HeadsIcon = await res3.text();

        // import the SVG for the Tails Coin
        const res4 = await fetch('public/assets/tails-big.svg');
        TailsIcon = await res4.text();
    });


    // Create Logic to assign Head or Tails to the selection
    let scenario = 0;           // scenario is either 6, 10 or 20
    let counter = 0;
    let {mean_heads, mean_tails} : Record<string, Record<string,number>> =
    {
        "mean_heads": {
        "throw_1": 33.33333333333333,
          "throw_2": 100,
          "throw_3": 33.33333333333333,
          "throw_4": 33.33333333333333,
          "throw_5": 33.33333333333333,
          "throw_6": 66.66666666666666,
          "throw_7": 33.33333333333333,
          "throw_8": 100
    },
        "mean_tails": {
        "throw_1": 66.66666666666666,
          "throw_2": 0,
          "throw_3": 66.66666666666666,
          "throw_4": 66.66666666666666,
          "throw_5": 66.66666666666666,
          "throw_6": 33.33333333333333,
          "throw_7": 66.66666666666666,
          "throw_8": 0
    }
    }
    // Selection as Dict for API-call and Array for display
    let selection: Record<string, string | null> = {};
		let selection_array: { id: string; value: string | null }[] = [];

    // Fill up the selection with null values when the scenario changes
    $: for (let i = 1; i <= scenario; i++) {
        selection[`throw_${i}`] = null;
    }

    // Change the selection from dictionary to array to display
    $: {
			let keys: string[] = Object.keys(selection).map(String);
        let coin: (string | null)[] = Object.values(selection);

        selection_array =
          coin.map((item: (string | null), index: number) => {
              return { id: keys[index], value: item };
          });
    }

    // Function to send POST Request to Backend
    function PostSelection() {
        // prepare Data to send to Backend
        let data = selection;
        console.log(data);
        // Send POST Request to Backend
			fetch(`http://127.0.0.1:8000/throws/${scenario}/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        })
          .then(response => response.json())
          .then(data => {
              console.log('Success:', data);
          })
          .catch((error) => {
              console.error('Error:', error);
          })
          .finally(() => {
              scenario = 0;
              counter = 0;
              selection = {};
          });
    }

</script>

<!-- ===============================[ Hero section ]========================================= -->

<section class="pt-8 flex content-center justify-center">
    <div class="w-2/3 flex mobile:flex-col h-min-[80vh] mt-[10vh]">
        <div class="w-1/2 h-full flex items-center ">
            <div class="prose font-default">
                <h1 class="my-3" id="#title">Münzwurf</h1>
                <h3 class="my-2">Die Wahrscheinlichkeiten eines Münzwurf</h3>
                <p>
                    Finde mit uns heraus wie die Statistik eines Münzwurfs aussieht und wie wir Menschen diese
                    Wahrscheinlichkeiten einschätzen.
                </p>
                <div class="pt-3 my-6">
                    <a class="btn-outer" href="#Münzwurf">Zum Münzwurf</a>
                </div>
            </div>
        </div>
        <div class="w-1/2 h-fit">
            <div class="h-fit">
                <!-- eslint-disable-next-line svelte/no-at-html-tags -->
                {@html svgHero}
            </div>
        </div>
    </div>
</section>

<!-- ===============================[ Explanation section ]====================================== -->

<section class="flex items-center justify-center">
    <div class="w-3/4 flex h-[60vh] justify-center items-center gap-5">
        <div class="w-1/2">
            <div class="w-fit">
                <!-- eslint-disable-next-line svelte/no-at-html-tags -->
                {@html svgTask}
            </div>
        </div>
        <div class="w-1/2 h-full flex items-center">
            <div class="prose font-default">
                <h1 class="my-3" id="#title">Unser Ziel</h1>
                <p>
                    Wir wollen zusammen herausfinden, wie eine Person den Zufall einschätzen. Kommt zuerst Kopf? Zahl?
                    Wie oft denkst du denn kann ein Ergebnis hintereinander vorkommen?
                    Untersuche mit uns wie wir den Zufall auffassen und wie du einen Münzwurf einschätzt.
                </p>
            </div>
        </div>
    </div>
</section>

<!-- ======================================[ Task section ]======================================== -->

<section id="Münzwurf" class="pt-8 flex content-center justify-center mb-20">
    <div class="w-3/4 flex h-[80vh] justify-center content-center gap-5">
        <!-- If no scenario has been selected -->
        {#if scenario === 0}
    
            <div class="h-full flex justify-center items-center " in:fade>
                <div class="prose font-default">
                    <h1 class="my-3">Deine Aufgabe</h1>
                    <p>
                        Entscheide wie oft du die Münze werfen willst und wähle zwischen Kopf oder Zahl.
                    </p>
                    {#if scenario !== 0}
                        <p id="click">clicked</p>
                    {/if}
                    <!-- TODO: Adjust the button to the same size as the other buttons -->
                    <div class="pt-3 my-6 w-fit flex flex-wrap gap-2 justify-center">
                        <button class="btn-outer" on:click={() => {scenario = 8}} id="8">&nbsp 8-Mal werfen</button>
                        <button class="btn-outer" on:click={() => {scenario = 10}} id="10">10-Mal werfen</button>
                        <button class="btn-outer" on:click={() => {scenario = 20}} id="20">20-Mal werfen</button>
                    </div>
                </div>
            </div>

            <div class="w-1/2 flex justify-center items-center">
                <div class="h-fit w-fit flex content-center justify-center">
                    <!-- eslint-disable-next-line svelte/no-at-html-tags -->
                    {@html svgTask}
                </div>
            </div>
            <!-- If scenario has been selected and User is selecting Heads or Tails -->
        {:else if scenario >= 8 && counter !== scenario}
            <div class="flex flex-col h-full justify-center gap-24" in:fade>
                <!-- TODO: Create Head or Tails selection Card -->
                <div class="flex flex-row gap-32 justify-center items-center">
                    <button
                      class="btn-outer bg-background w-[270px] h-min-[350px] flex flex-col items-center justify-center gap-5 font-default"
                      id="Kopf-selection"
											on:click={() => {counter += 1; selection[`throw_${counter}`] ="heads";}}>
                        <span class="w-[250px] h-[250px]">{@html HeadsIcon}</span>
                        <span class="font-default prose-xl font-bold">Kopf</span>
                    </button>
                    <h1 class="prose text-4xl font-bold font-default">Oder</h1>
                    <button
                      class="btn-outer bg-background w-[270px] h-min-[350px] flex flex-col items-center justify-center gap-5 "
                      id="Zahl-selection"
											on:click={() => {counter += 1; selection[`throw_${counter}`] ="tails";}}>
                        <span class="w-[250px] h-[250px]">{@html TailsIcon}</span>
                        <span class="font-default prose-xl font-bold">Zahl</span>
                    </button>
                </div>
                <SelectionList selection_array={selection_array}></SelectionList>
            </div>

            <!-- Last Heads or Tails has been selected. Ready to review and submit -->
        {:else if counter === scenario}
            <div class="flex flex-col justify-center items-center gap-20" in:fade>

                <h1 class="prose text-4xl font-bold font-default">Fertig!</h1>
                <SelectionList selection_array={selection_array}></SelectionList>
                <button class="btn-outer prose text-xl font-bold font-default bg-background"
                        on:click={PostSelection}>
                    Bestätigen
                </button>

            </div>
        {/if}
    </div>
</section>

<!-- ===============================[ Analysis section ]====================================== -->

<section class="mb-20 flex items-center justify-center">
    <div class="w-3/4 flex h-[60vh] justify-center items-center gap-5">
        <div class="w-1/2 h-full border-y border-l flex flex-col justify-around">
            {#each Object.keys(mean_heads) as key, index}
                <div class="w-full flex h-full">
                    <div class="w-fit px-3 border-r content-center"><h1>{index}: </h1></div>
                    <div style="width: {mean_heads[key]}%;" class="bg-secondary h-full overflow-hidden content-center border-y"><p class="px-5">Heads: {mean_heads[key].toFixed(2)} %</p></div>
                    <div style="width: {mean_tails[key]}%;" class="bg-primary h-full overflow-hidden content-center border-y"><p class="px-5">Tails: {mean_tails[key].toFixed(2)} %</p></div>
                </div>
            {/each}
        </div>
        <div class="w-1/2 h-full flex items-center">
            <div class="prose font-default">
                <h1 class="my-3" id="#title">Analyse</h1>
                <p>
                    Wir wollen zusammen herausfinden, wie eine Person den Zufall einschätzen. Kommt zuerst Kopf? Zahl?
                    Wie oft denkst du denn kann ein Ergebnis hintereinander vorkommen?
                    Untersuche mit uns wie wir den Zufall auffassen und wie du einen Münzwurf einschätzt.
                </p>
            </div>
        </div>
    </div>
</section>

