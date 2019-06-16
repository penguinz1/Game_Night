const make_randoms_test = () => {
    let maximum = 20;
    let randoms = make_randoms(maximum, 0, 5);

    for (let i = 0; i < randoms.length; i++) {
        if (randoms[i][0] < 0 || randoms[i][0] > maximum) {
            console.log("FAIL: make_randoms_test");
            success = false;
            return;
        }
    }
}

const make_random_test = () => {
    let randoms = [];
    let maximum = 20;

    for (let i = 0; i < 50; i++) {
        randoms.push(make_random(maximum, i));
    }

    for (let i = 0; i < randoms.length; i++) {
        if (randoms[i][0] < 0 || randoms[i][0] > maximum) {
            console.log("FAIL: make_random_test");
            success = false;
            return;
        }
    }
}

const make_groups_test = () => {
    let group_list = ["a", "b", "c", "d", "e", "f"];
    let splits = make_groups(group_list, 0, 3)[0];

    if (splits.length !== 3) {
        console.log("FAIL: make_groups_test");
        success = false;
        return;
    }

    for (let i = 0; i < splits.length; i++) {
        if (splits[i].length !== 2) {
            console.log("FAIL: make_groups test");
            success = false;
            return;
        }
    }
}

const extensive_make_groups_test = () => {
    for (let i = 0; i < 100; i++) {
        let group_size = make_random(100, i)[0] + 5;
        let n_splits = make_random(2, i + 1)[0] + 2;
        let split_size = Math.floor(group_size / n_splits);

        let group_list = [];
        for (let j = 0; j < group_size; j++) {
            group_list.push("test");
        }

        let splits = make_groups(group_list, i + 2, n_splits)[0];
        for (let j = 0; j < splits.length; j++) {
            let split = splits[j];
            if (split.length !== split_size && split.length !== split_size + 1) {
                console.log("FAIL: extensive_make_groups_test");
                success = false;
                return;
            }
        }
    }
}

const run_random_test = () => {
    make_random_test();
    make_randoms_test();
    make_groups_test();
    extensive_make_groups_test();
}