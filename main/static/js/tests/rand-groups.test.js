const get_two_power_test = () => {
    if (get_two_power(2) !== 1) {
        console.log("FAIL: get_two_power_test");
        success = false;
        return;
    }

    if (get_two_power(16) !== 4) {
        console.log("FAIL: get_two_power_test");
        success = false;
        return;
    }

    if (get_two_power(1024) !== 10) {
        console.log("FAIL: get_two_power_test");
        success = false;
        return;
    }
}

const get_rand_test = () => {
    let randoms = []
    let power = 5

    for (let i = 0; i < 50; i++) {
        randoms.push(get_rand(power, i, 0))
    }

    for (let i = 0; i < randoms.length; i++) {
        if (randoms[i][0] < 0 || randoms[i][0] > Math.pow(2, power) - 1) {
            console.log("FAIL: get_rand_test");
            success = false;
            return;
        }
    }
}

const convert_list_test = () => {
    let argument = "amy jim john"
    let expected = ["amy", "jim", "john"]
    let actual = convert_list(argument)

    if (expected.length !== actual.length) {
        console.log("FAIL: convert_list_test");
        success = false;
        return; 
    }

    for (let i = 0; i < expected.length; ++i) {
        if (actual[i] !== expected[i]) {
            console.log("FAIL: convert_list_test");
            success = false;
            return;
        }
    }
}

const run_rand_groups_test = () => {
    get_two_power_test();
    get_rand_test();
    convert_list_test();
}