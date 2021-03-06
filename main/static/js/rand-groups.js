const MAX_GROUPS = 4; // max number of groups

var raw_groups = document.getElementById("groups"); // group list in text form
var num_groups = document.getElementById("num-groups"); // number of groups to generate
var group_submit = document.getElementById("pick-groups"); // submit button

// graciously provided by Stack Overflow:
// https://stackoverflow.com/questions/11128700/create-a-ul-and-fill-it-based-on-a-passed-array
// creates an unordered list html object from an arrays
function makeUL(array) {
    // Create the list element:
    var list = document.createElement('ul');

    for (var i = 0; i < array.length; i++) {
        // Create the list item:
        var item = document.createElement('li');

        // Set its contents:
        item.appendChild(document.createTextNode(array[i]));

        // Add it to the list:
        list.appendChild(item);
    }

    // Finally, return the constructed list:
    return list;
}

// gets the x that solves 2^x = num (gets the power of 2 of num)
const get_two_power = (num) => {
    if (num <= 2) {
        return 1;
    }

    return 1 + get_two_power(num / 2);
}

// gets a random number in the interval [0, 2^power - 1]
const get_rand = (power, rand_ind, total) => {
    if (power == 1) {
        return heads_tails(rand_ind) ? [total + 1, rand_ind + 1] : [total, rand_ind + 1]
    }

    if (heads_tails(rand_ind)) {
        return get_rand(power - 1, rand_ind + 1, total + power);
    } else {
        return get_rand(power - 1, rand_ind + 1, total);
    }
}

// converts the raw group list text into an array
const convert_list = (raw) => {
    return raw.split(/[\W]+/);
}

// generates groups from the group_list
const gen_groups = (group_list, rand_ind, n_groups, is_even) => {
    if (is_even) {
        return make_groups(group_list, rand_ind, n_groups)
    } else {
        let groups = []
        for (let i = 0; i < n_groups; i++) {
            groups.push([]);
        }

        for (let i = 0; i < group_list.length; i++) {
            let bucket = get_rand(get_two_power(n_groups), rand_ind, 0);
            groups[bucket[0]].push(group_list[i]);

            rand_ind = bucket[1];
        }

        return [groups, rand_ind];
    }
}

// cleans existing html lists
const getAndCleanLists = (n_groups) => {
    let lists = []

    for (let i = 1; i <= MAX_GROUPS; i++) {
        let elem = document.getElementById("group" + i);
        while (elem.firstChild) {
            elem.removeChild(elem.firstChild);
        }
        if (i <= n_groups) {
            lists.push(elem);
        }
    }

    return lists;
}

// updates the html lists to show the groups generated
group_submit.addEventListener("click", () => {
    let n_groups = parseInt(num_groups.value);
    if (n_groups > MAX_GROUPS) {
        n_groups = MAX_GROUPS;
    }

    let is_even = document.querySelector('input[name="gen-type"]:checked').value == "even";
    console.log(is_even);
    if (!is_even && n_groups != 2 && n_groups != 4) {
        n_groups = 2
    }

    let r_ind = parseInt(focus.value);
    let lists = getAndCleanLists(n_groups);
    let groups = gen_groups(convert_list(raw_groups.value), r_ind, n_groups, is_even);

    for (let i = 0; i < n_groups; i++) {
        let list = makeUL(groups[0][i]);
        lists[i].appendChild(list);
    }

    focus.value = groups[1]; // updates random index
    num_groups.value = n_groups; // updates number of groups field
});