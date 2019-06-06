const runtests = () => {
    run_rand_groups_test();
    run_random_test();
    run_space_game_test();

    if (success) {
        console.log("All Tests Passed!")
    }
    return success
}