const runtests = () => {
    run_rand_groups_test();
    run_random_test();

    if (success) {
        console.log("All Tests Passed!")
    }
    return success
}