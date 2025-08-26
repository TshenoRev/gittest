def main():
    game_state = GameState("path/to/config_file.txt")

    while True:
        print(f"Player {game_state.current_player}'s turn:")
        move = input("Enter your move: ")
        
        if move == 'q':
            print("Game ended via quit.")
            break
        
        try:
            game_state.handle_move(move)
            game_state.write_output(f"Player {game_state.current_player} performed the move {move}")
            
            if game_state.check_win():
                print(f"Player {game_state.current_player} wins!")
                break
            
            if game_state.check_draw():
                print("Game ended in a draw.")
                break
            
            # Switch players
            game_state.current_player = 2 if game_state.current_player == 1 else 1
        
        except Exception as e:
            game_state.write_output(str(e))
            print("Invalid move, please try again.")

if __name__ == '__main__':
    main()
