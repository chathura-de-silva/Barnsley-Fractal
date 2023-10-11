using JSON
default_preferences = Dict(
    "ultrafast" => true,
    "x_offset" => 0,
    "y_offset" => -230,
    "scale" => 50,
    "plot_points" => 10000,
    "probabilities" => [0.01, 0.85, 0.07, 0.07],
    "x" => 0,
    "y" => 0,
    "speed" => 0,
    "leftleaf_color" => "#6E4C21",
    "rightleaf_color" => "#37B469",
    "base_color" => "#988a4f",
    "top_color" => "#788511",
    "completion_message" => nothing,  # Julia's equivalent to None
    "background_color" => "black",
    "save_image" => false,
    "point_size" => 1,
    "use_dot_points" => false
)

# #Definition of the function to check the command line arguments.
function check_cmd_args(sys_args, arg_count)
    global preferences
    if arg_count > 0 & sys_args[1] == "-s"
        preferences["ultrafast"] = false
        print("plotting in slow mode.")
        if arg_count == 2
            preferences["speed"] = parse(Int, sys_args[2])
        end

    elseif arg_count == 1 & sys_args[1] == "-u"
        preferences["ultrafast"] = true
        print("plotting in ultrafast mode.")

    elseif arg_count == 1 & sys_args[1] == "save"
        preferences["save_image"] = true

    elseif arg_count == 2 & sys_args[1] == "-p" & args[2].isdigit()
        preferences["plot_points"] = parse(Int, sys_args[2])
        print("plotting ", sys_args[2], " points.")

    elseif arg_count == 1 & sys_args[1] == "-h"
        print("Refer the README.md file for more information.")
        exit()

    elseif arg_count > 1 & sys_args[1] == "-c"
        for arg in sys_args[2:end]
            if length(arg) == 9 & arg[3] == "#" & (parse(Int, arg[4:end], base=16) < 16777216)
                if arg[1:2] == "ll"
                    preferences["leftleaf_color"] = arg[4:end]
                elseif arg[1:2] == "rl"
                    preferences["rightleaf_color"] = arg[4:end]
                elseif arg[1:2] == "bs"
                    preferences["base_color"] = arg[4:end]
                elseif arg[1:2] == "tp"
                    preferences["top_color"] = arg[4:end]
                end
            end
        end
    elseif arg_count == 1 & sys_args[1] == "reset"
        preferences = default_preferences
        print("Preferences reset to default.")
    end
end
# Definitions of the functions for the fractal transformations.
function function1(x, y)
    return [0.0 0.0; 0.0 0.16] * [x; y]
end

function function2(x, y)
    return [0.85 0.04; -0.04 0.85] * [x; y] + [0.0; 1.6]
end

function function3(x, y)
    return [0.2 -0.26; 0.23 0.22] * [x; y] + [0.0; 1.6]
end

function function4(x, y)
    return [-0.15 0.28; 0.26 0.24] * [x; y] + [0.0; 0.44]
end
#End of the function definitions.

# Loading preferences from the preferences from the JSON file if there is any.
try
    global preferences = JSON.parsefile("preferences_barnsley.json")
    print("prefs: "*preferences)
catch e
    if isa(e, SystemError) occursin("no such file", string(e))  # Julia's equivalent to FileNotFoundError
        println("The file 'preferences_barnsley.json' does not exist. Using default preferences.")
        global preferences = default_preferences
    else
        println("Error: ", e) 
        println("Stacktrace: ", catch_backtrace())
    end
end
