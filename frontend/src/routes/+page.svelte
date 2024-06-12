<script lang="ts">
    import { onMount } from 'svelte';
    import SelectionList from '../components/SelectionList.svelte'; // Adjusted import
    import { fade } from'svelte/transition';
    import Analysis from "../components/Analysis.svelte";
    import {writable} from "svelte/store";

    // Scenario options
    let scenarioOptions = [8, 10, 20, 30]
    // SVG names
    let svgHero: string = '';
    let svgTask: string = '';
    let svgCoinTask: string = '';
    let HeadsIcon: string = '';
    let TailsIcon: string = '';
    let svgAnalysis: string = '';


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

        // import the SVG for the Tails Coin
        const res5 = await fetch('public/assets/Coin-task.svg');
        svgCoinTask = await res5.text();

        // import the SVG for the hero section
        const res6 = await fetch('public/assets/Stats-Analysis.svg');
        svgAnalysis = await res6.text();
    });

    // Create a writable store
    let fetchTrigger = writable(false);

    // Function to set fetchTrigger to true
    function handleClick() {
        fetchTrigger.set(true);
    }
    // Create Logic to assign Head or Tails to the selection
    let scenario: number = 0;           // scenario is either 6, 10 or 20
    let counter: number = 0;
    let analysisOption: number = scenarioOptions[0];          // analysis is either 8, 10, 20 or any of the array of the scenarioOptions

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
        fetch(`/throws/${scenario}`, {
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
              handleClick();
          });
    }

</script>

<!-- ===============================[ Hero section ]========================================= -->
{#key scenario}
    <section class="pt-8 flex content-center justify-center desktop:h-auto desktop:pt-0">
        <div class="w-2/3 flex desktop:flex-col-reverse h-min-[80vh] mt-[10vh] desktop:h-screen desktop:w-full desktop:mt-0">
            <div class="w-1/2 h-full flex flex-col justify-center desktop:w-full desktop:items-center">
                <div class="prose font-default desktop:text-center">
                    <h1 class="my-3" id="#title">Münzwurf</h1>
                    <h3 class="my-2">Die Wahrscheinlichkeiten eines Münzwurf</h3>
                    <p>
                        Finde mit uns heraus wie die Statistik eines Münzwurfs aussieht und wie wir Menschen diese
                        Wahrscheinlichkeiten einschätzen.
                    </p>
                </div>
                <div class="pt-3 my-6">
                    <a class="btn-outer" href="#Münzwurf">Zum Münzwurf</a>
                </div>
            </div>

            <div class="w-1/2 h-min desktop:w-full desktop:max-h-[50vh]">
                <div class=" desktop:h-fit desktop:flex desktop:items-center desktop:justify-center desktop:max-h-[50vh]">
                    <!-- eslint-disable-next-line svelte/no-at-html-tags -->
                    {@html svgHero}
                </div>
            </div>
        </div>
    </section>
{/key}
<!-- ===============================[ Explanation section ]====================================== -->
<section class="my-8 flex content-center justify-center desktop:h-auto desktop:mb-14" transition:fade>
    <div class="w-3/4 flex h-[60vh] justify-center items-center gap-5 desktop:h-auto desktop:flex-col">
        <div class="w-1/2 h-fit desktop:w-full">
            <div class="h-fit flex items-center justify-center">
                <!-- eslint-disable-next-line svelte/no-at-html-tags -->
                {@html svgTask}
            </div>
        </div>
        <div class="w-1/2 h-full flex justify-center items-center desktop:w-full">
            <div class="prose font-default desktop:text-center">
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
{#key scenario}
    <section id="Münzwurf" class="my-8 flex content-center justify-center desktop:h-auto desktop:mb-14" transition:fade>
        <div class="w-3/4 flex h-[70vh] justify-center content-center gap-5 desktop:h-auto">
        <!-- If no scenario has been selected -->
        {#if scenario === 0}
    
            <div class="h-full flex justify-center items-center " in:fade>
                <div class="prose font-default desktop:text-center">
                    <h1 class="my-3">Deine Aufgabe</h1>
                    <p>
                        Entscheide wie oft du die Münze werfen willst und wähle zwischen Kopf oder Zahl.
                    </p>
                    {#if scenario !== 0}
                        <p id="click">clicked</p>
                    {/if}
                    <!-- TODO: Adjust the button to the same size as the other buttons -->
                    <div class="pt-3 my-6 w-fit flex flex-wrap gap-2 justify-center">
                        {#each scenarioOptions as value}
                            <button class="btn-outer" on:click={() => {scenario = value}} id="{value}">&nbsp {value}-Mal
                                werfen
                            </button>
                        {/each}
                    </div>
                </div>
            </div>

            <div class="w-1/2 flex justify-center items-center desktop:hidden">
                <div class="h-fit w-fit flex content-center justify-center">
                    <!-- eslint-disable-next-line svelte/no-at-html-tags -->
                    {@html svgCoinTask}
                </div>
            </div>
            <!-- If scenario has been selected and User is selecting Heads or Tails -->
        {:else if scenario != 0 && counter !== scenario}
            <div class="flex flex-col h-full justify-center gap-24 desktop:gap-5" in:fade>
                <div class="flex flex-row gap-32 justify-center items-center desktop:gap-14">
                    <button
                            class="btn-outer bg-background w-[270px] h-min-[350px] desktop:w-1/3 flex flex-col items-center justify-center gap-5 font-default"
                      id="Kopf-selection"
											on:click={() => {counter += 1; selection[`throw_${counter}`] ="heads";}}>
                        <span class="w-[250px] h-[250px] desktop:hidden">{@html HeadsIcon}</span>
                        <span class="font-default prose-xl font-bold">Kopf</span>
                    </button>
                    <h1 class="prose text-4xl font-bold font-default desktop:hidden">Oder</h1>
                    <button
                            class="btn-outer bg-background w-[270px] h-min-[350px] desktop:w-1/3 flex flex-col items-center justify-center gap-5 "
                      id="Zahl-selection"
											on:click={() => {counter += 1; selection[`throw_${counter}`] ="tails";}}>
                        <span class="w-[250px] h-[250px] desktop:hidden">{@html TailsIcon}</span>
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
{/key}


<!-- ===============================[ Analysis intro section ]========================================= -->
<section class="my-8 flex content-center justify-center desktop:h-auto desktop:mb-14" transition:fade>
    <div class="w-3/4 flex h-[60vh] justify-center items-center gap-5 desktop:h-auto desktop:flex-col">
        <div class="w-1/2 h-fit desktop:w-full">
            <div class="h-fit">
                <!-- eslint-disable-next-line svelte/no-at-html-tags -->
                {@html svgAnalysis}
            </div>
        </div>
        <div class="w-1/2 h-full flex justify-center items-center desktop:w-full">
            <div class="prose font-default desktop:text-center">
                <h1 class="my-3" id="#title">Analyse</h1>
                <p>
                    Wir wollen zusammen herausfinden, wie eine Person den Zufall einschätzen. Kommt zuerst Kopf?
                    Zahl?
                    Wie oft denkst du denn kann ein Ergebnis hintereinander vorkommen?
                    Untersuche mit uns wie wir den Zufall auffassen und wie du einen Münzwurf einschätzt.
                </p>
            </div>
        </div>
        <div class="pt-3 my-6 w-fit flex flex-wrap gap-2 justify-center">
            {#each scenarioOptions as value}
                <button class="btn-outer" on:click={() => {analysisOption = value; handleClick()}}>&nbsp {value}-Würfe
                    analysieren
                </button>
            {/each}
        </div>
    </div>
</section>

<!-- ===============================[ Analysis section ]====================================== -->
<Analysis analysis={analysisOption} {fetchTrigger}></Analysis>


