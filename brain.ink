inkling "2.0"
using Goal
using Math

const step_size = 20

const SimulatorVisualizer = "https://microsoft.github.io/bonsai-rgb/visualizer/"

type SimConfig {
    C: number<0 .. 100 step 1>,
    M: number<0 .. 100 step 1>,
    Y: number<0 .. 100 step 1>,
    K: number<0 .. 100 step 1>,
    R: number<0 .. 255 step 1>,
    G: number<0 .. 255 step 1>,
    B: number<0 .. 255 step 1>
}

type SimState {
    target_C: number<0 .. 100 step 1>,
    target_M: number<0 .. 100 step 1>,
    target_Y: number<0 .. 100 step 1>,
    target_K: number<0 .. 100 step 1>,
    current_red: number<0 .. 255 step 1>,
    current_green: number<0 .. 255 step 1>,
    current_blue: number<0 .. 255 step 1>,
    Mean_Absolute_Error: number,
    delta1: number,
    delta2: number,
    delta3: number,
    delta4: number
}

type Action {
    delta_red: number<-step_size .. step_size step 1>,
    delta_green: number<-step_size .. step_size step 1>,
    delta_blue: number<-step_size .. step_size step 1>
}
simulator Simulator(Action: Action, Config: SimConfig): SimState {
    package "rgb-sim"
}

graph (input: SimState): Action {
    concept Concept(input): Action {
        curriculum {
            source Simulator

            training {
                EpisodeIterationLimit: 50,
                NoProgressIterationLimit: 1000000
            }

            goal (state: SimState) {
                reach low_MAE:
                    state.Mean_Absolute_Error
                    in Goal.RangeBelow(1)
            }

            lesson `All Colors` {
                scenario {
                    C: number<0 .. 100 step 1>,
                    M: number<0 .. 100 step 1>,
                    Y: number<0 .. 100 step 1>,
                    K: number<0 .. 100 step 1>,
                    R: number<0>,
                    G: number<0>,
                    B: number<0>
                }
            }
        }
    }
}

